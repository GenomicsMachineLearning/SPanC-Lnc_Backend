import io as io
import pathlib as pathlib
import threading
import urllib as urllib

import alphagenome.data.gene_annotation as alphagenome_data_gene_annotation
import alphagenome.data.genome as alphagenome_data_genome
import alphagenome.data.transcript as alphagenome_data_transcript
import alphagenome.models.dna_client as alphagenome_dna_client
import alphagenome.models.dna_output as alphagenome_dna_output
import \
    alphagenome.visualization.plot_components as alphagenome_visualization_plot_components
import django.http.response as http_response
import django.utils.decorators as django_decorators
import django.views.decorators.csrf as django_views_csrf
import matplotlib as matplotlib
import matplotlib.pyplot as matplotlib_plt
import pandas as pd
from django import views as django_views
from django.http import JsonResponse

from Incrna import settings
from ..genomic_utils import parse_genomic_coordinates

matplotlib.use('Agg')  # Use non-interactive backend


@django_decorators.method_decorator(django_views_csrf.csrf_exempt, name='dispatch')
class AlphaGenomeView(django_views.View):
    # Class-level attributes
    ontology_terms = ['UBERON:0001155']  # COLON
    organism = alphagenome_dna_client.Organism.HOMO_SAPIENS
    gtf_filename = 'gencode.v46.annotation.gtf.gz.feather'
    gtf_url = f'https://storage.googleapis.com/alphagenome/reference/gencode/hg38/{gtf_filename}'
    _analysis_lock = threading.Lock()
    _api_key = settings.ALPHA_GENOME_API_KEY

    @property
    def gtf_local_path(self):
        data_dir = settings.DATA_DIR
        return pathlib.Path(data_dir) / self.gtf_filename

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

        # Ensure GTF data is loaded
        self.download_gtf_if_needed()
        gtf_data = pd.read_feather(self.gtf_local_path)
        longest_transcript_extractor = self._load_gtf_data(gtf_data)

        # Your AlphaGenome code
        new_start, new_stop, new_len = self._adjust_interval_with_extra_base(
            start, stop)
        interval = alphagenome_data_genome.Interval(chromosome=chr, start=new_start,
                                                    end=new_stop)

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

        longest_transcripts = longest_transcript_extractor.extract(interval)
        return self._plot_to_png_response(interval, output, longest_transcripts)

    def download_gtf_if_needed(self):
        local_path = self.gtf_local_path
        if local_path.exists():
            print(f"GTF file already exists at {local_path}")
            return
        local_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            urllib.request.urlretrieve(self.gtf_url, local_path)
        except Exception as e:
            raise Exception(f"Failed to download GTF file: {str(e)}")

    @staticmethod
    def _load_gtf_data(gtf_data):
        # Filter to protein-coding genes and highly supported transcripts
        gtf_transcript = alphagenome_data_gene_annotation.filter_transcript_support_level(
            alphagenome_data_gene_annotation.filter_protein_coding(gtf_data), ['1']
        )
        # Create extractors
        gtf_longest_transcript = alphagenome_data_gene_annotation.filter_to_longest_transcript(
            gtf_transcript)
        longest_transcript_extractor = alphagenome_data_transcript.TranscriptExtractor(
            gtf_longest_transcript)
        return longest_transcript_extractor

    @staticmethod
    def _plot_to_png_response(interval, output, longest_transcripts):
        try:
            matplotlib_plt.clf()
            matplotlib_plt.close('all')

            fig = alphagenome_visualization_plot_components.plot(
                [
                    alphagenome_visualization_plot_components.TranscriptAnnotation(
                        longest_transcripts),
                    alphagenome_visualization_plot_components.Tracks(
                        tdata=output.splice_sites,
                        ylabel_template='SPLICE SITES: {name} ({strand})',
                    ),
                ],
                interval=interval,
                title='Predicted splicing effects for Colon tissue',
            )

            buffer = io.BytesIO()
            fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            content = buffer.getvalue()
            buffer.close()
            matplotlib_plt.close(fig)
            new_buffer = io.BytesIO(content)
            response = http_response.HttpResponse(new_buffer, content_type='image/png')
            return response
        except Exception as e:
            matplotlib_plt.close()  # Ensure figure is closed even if there's an error
            raise e

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
