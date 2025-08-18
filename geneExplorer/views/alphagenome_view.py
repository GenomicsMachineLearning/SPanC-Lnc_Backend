import pandas as pd
import threading
from django import views as django_views
from django.views import decorators as django_decorators
from django.views.decorators import csrf as django_views_csrf
from django.http import JsonResponse
from Incrna import settings
import alphagenome.data as alphagenome_data
import alphagenome.models as alphagenome_models
import alphagenome.visualization as alphagenome_visualization
import matplotlib.pyplot as plt
import django.conf as django_conf

@django_decorators.method_decorator(django_views_csrf.csrf_exempt, name='dispatch')
class AlphaGenomeView(django_views.View):
    # Class-level attributes
    ontology_terms = ['UBERON:0001155']  # COLON
    gtf_url = 'https://storage.googleapis.com/alphagenome/reference/gencode/hg38/gencode.v46.annotation.gtf.gz.feather'
    _analysis_lock = threading.Lock()
    # Cache GTF data at class level to avoid reloading
    _gtf_data = None
    _transcript_extractor = None
    _longest_transcript_extractor = None

    def get(self, request):
        # Get parameters from request
        chr = request.GET.get('chr', 'chr8')
        start = int(request.GET.get('start', 21445867))
        stop = int(request.GET.get('stop', 21447688))

        try:
            with self._analysis_lock:
                return self._do_alphagenome_analysis(chr, start, stop)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    def _do_alphagenome_analysis(self, chr, start, stop):
        dna_model = alphagenome_models.create(settings.ALPHA_GENOME_API_KEY)

        # Initialize GTF data if not already loaded
        if self._gtf_data is None:
            self._load_gtf_data()

        # Your AlphaGenome code
        new_start, new_stop, new_len = self._adjust_interval_with_extra_base(
            start, stop)
        interval = alphagenome_data.Interval(chromosome=chr, start=new_start, end=new_stop)

        # Make predictions
        output = dna_model.predict_interval(
            interval=interval,
            requested_outputs={
                alphagenome_models.OutputType.RNA_SEQ,
                alphagenome_models.OutputType.SPLICE_SITES,
                alphagenome_models.OutputType.SPLICE_SITE_USAGE,
                alphagenome_models.OutputType.SPLICE_JUNCTIONS,
            },
            ontology_terms=self.ontology_terms,
        )

        longest_transcripts = self._longest_transcript_extractor.extract(interval)

        # Build plot
        plot = alphagenome_visualization.plot(
            [
                alphagenome_visualization.TranscriptAnnotation(longest_transcripts),
                alphagenome_visualization.Tracks(
                    tdata=output.splice_sites,
                    ylabel_template='SPLICE SITES: {name} ({strand})',
                ),
            ],
            interval=interval,
            title='Predicted splicing effects for Colon tissue',
        )

        return JsonResponse({
            'success': True,
            'interval': f"{chr}:{new_start}-{new_stop}",
            'splice_sites_count': len(output.splice_sites.data) if hasattr(
                output.splice_sites, 'data') else 0,
            'transcripts_count': len(longest_transcripts),
            # Add other data you need
        })

    @staticmethod
    def _adjust_interval_with_extra_base(start: int, stop: int):
        target_lengths = [2048, 16384, 131072, 524288, 1048576]
        current_length = stop - start + 1
        larger_or_equal = [l for l in target_lengths if l >= current_length]
        if larger_or_equal:
            closest_length = min(larger_or_equal)
        else:
            closest_length = max(target_lengths)
        # Add one extra base to the chosen length
        adjusted_length = closest_length + 1
        new_stop = start + adjusted_length - 1
        # Double check length
        final_length = new_stop - start + 1
        return start, new_stop, final_length

    def _load_gtf_data(self):
        """Load and cache GTF data"""
        self._gtf_data = pd.read_feather(self.gtf_url)

        # Filter to protein-coding genes and highly supported transcripts
        gtf_transcript = alphagenome_data.filter_transcript_support_level(
            alphagenome_data.filter_protein_coding(self._gtf_data), ['1']
        )

        # Create extractors
        self._transcript_extractor = alphagenome_data.transcript.TranscriptExtractor(gtf_transcript)
        gtf_longest_transcript = alphagenome_data.gene_annotation.filter_to_longest_transcript(
            gtf_transcript)
        self._longest_transcript_extractor = alphagenome_data.transcript.TranscriptExtractor(
            gtf_longest_transcript)