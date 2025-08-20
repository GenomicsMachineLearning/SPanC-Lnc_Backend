import io as io
import pandas as pd
import threading
from django import views as django_views
import django.http.response as http_response
from django.http import JsonResponse
from Incrna import settings
from ..genomic_utils import parse_genomic_coordinates
import alphagenome.data.genome as alphagenome_data_genome
import alphagenome.data.gene_annotation as alphagenome_data_gene_annotation
import alphagenome.data.transcript as alphagenome_data_transcript
import alphagenome.models.dna_client as alphagenome_dna_client
import alphagenome.models.dna_output as alphagenome_dna_output
import alphagenome.visualization.plot_components as alphagenome_visualization_plot_components
import matplotlib as matplotlib
import matplotlib.pyplot as matplotlib_plt
matplotlib.use('Agg')  # Use non-interactive backend
import django.utils.decorators as django_decorators
import django.views.decorators.csrf as django_views_csrf

@django_decorators.method_decorator(django_views_csrf.csrf_exempt, name='dispatch')
class AlphaGenomeView(django_views.View):
    # Class-level attributes
    ontology_terms = ['UBERON:0001155']  # COLON
    organism = alphagenome_dna_client.Organism.HOMO_SAPIENS
    gtf_url = 'https://storage.googleapis.com/alphagenome/reference/gencode/hg38/gencode.v46.annotation.gtf.gz.feather'
    _analysis_lock = threading.Lock()
    _api_key = settings.ALPHA_GENOME_API_KEY
    # Cache GTF data at class level to avoid reloading
    _gtf_data = None
    _transcript_extractor = None
    _longest_transcript_extractor = None

    def get(self, request):
        search_param = request.GET.get('search', None)
        chr_parsed, start_parsed, end_parsed = parse_genomic_coordinates(
            str(search_param)) if search_param else (None, None, None)
        chr = chr_parsed or 'chr8'
        start = start_parsed or 21445867
        stop = end_parsed or 21447688

        try:
            with self._analysis_lock:
                return self._do_alphagenome_analysis(chr, start, stop)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    def _do_alphagenome_analysis(self, chr, start, stop):
        dna_model = alphagenome_dna_client.create(self._api_key)

        # Initialize GTF data if not already loaded
        if self._gtf_data is None:
            self._load_gtf_data()

        # Your AlphaGenome code
        new_start, new_stop, new_len = self._adjust_interval_with_extra_base(
            start, stop)
        interval = alphagenome_data_genome.Interval(chromosome=chr, start=new_start, end=new_stop)

        # Make predictions
        output = dna_model.predict_interval(
            interval=interval,
            organism=self.organism,
            requested_outputs={
                alphagenome_dna_output.OutputType.RNA_SEQ,
                alphagenome_dna_output.OutputType.SPLICE_SITES,
                alphagenome_dna_output.OutputType.SPLICE_SITE_USAGE,
                alphagenome_dna_output.OutputType.SPLICE_JUNCTIONS,
            },
            ontology_terms=self.ontology_terms,
        )

        longest_transcripts = self._longest_transcript_extractor.extract(interval)

        # Build plot
        plot = alphagenome_visualization_plot_components.plot(
            [
                alphagenome_visualization_plot_components.TranscriptAnnotation(longest_transcripts),
                alphagenome_visualization_plot_components.Tracks(
                    tdata=output.splice_sites,
                    ylabel_template='SPLICE SITES: {name} ({strand})',
                ),
            ],
            interval=interval,
            title='Predicted splicing effects for Colon tissue',
        )
        return self._plot_to_png_response(plot, chr, new_start, new_stop)

    @staticmethod
    def _plot_to_png_response(plot, chr, start, stop):
        buffer = io.BytesIO()

        # Save the plot to the buffer as PNG
        plot.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)

        response = http_response.HttpResponse(buffer.getvalue(), content_type='image/png')
        response['Content-Disposition'] = \
            f'inline; filename="alphagenome_{chr}_{start}_{stop}.png"'

        matplotlib_plt.close(plot)

        return response

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
        AlphaGenomeView._gtf_data = pd.read_feather(self.gtf_url)

        # Filter to protein-coding genes and highly supported transcripts
        gtf_transcript = alphagenome_data_gene_annotation.filter_transcript_support_level(
            alphagenome_data_gene_annotation.filter_protein_coding(self._gtf_data), ['1']
        )

        # Create extractors
        AlphaGenomeView._transcript_extractor = alphagenome_data_transcript.TranscriptExtractor(gtf_transcript)
        gtf_longest_transcript = alphagenome_data_gene_annotation.filter_to_longest_transcript(
            gtf_transcript)
        AlphaGenomeView._longest_transcript_extractor = alphagenome_data_transcript.TranscriptExtractor(
            gtf_longest_transcript)