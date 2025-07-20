class AlphaGenome:

    def do_stuff(self):
        # Example usage:
        chr = 'chr8'  # user defined
        start = 21445867  # user defined
        stop = 21447688  # user defined
        new_start, new_stop, new_len = adjust_interval_with_extra_base(start, stop)
        interval = genome.Interval(chromosome=chr, start=new_start, end=new_stop)
        import pandas as pd

        # Load metadata objects for human.
        output_metadata = dna_model.output_metadata(
            organism=dna_client.Organism.HOMO_SAPIENS
        )
        # Load gene annotations (from GENCODE).
        gtf = pd.read_feather(
            'https://storage.googleapis.com/alphagenome/reference/gencode/'
            'hg38/gencode.v46.annotation.gtf.gz.feather'
        )
        # Filter to protein-coding genes and highly supported transcripts.
        gtf_transcript = gene_annotation.filter_transcript_support_level(
            gene_annotation.filter_protein_coding(gtf), ['1']
        )
        # Extractor for identifying transcripts in a region.
        transcript_extractor = transcript.TranscriptExtractor(gtf_transcript)
        # Also define an extractor that fetches only the longest transcript per gene.
        gtf_longest_transcript = gene_annotation.filter_to_longest_transcript(
            gtf_transcript
        )
        longest_transcript_extractor = transcript.TranscriptExtractor(
            gtf_longest_transcript
        )
        # List of IDs corresponding to various intestinal tissues.
        ontology_terms = [
            'UBERON:0001155',  # COLON
        ]
        # Make predictions for splicing outputs and RNA_SEQ.
        output = dna_model.predict_interval(
            interval=interval,
            requested_outputs={
                dna_client.OutputType.RNA_SEQ,
                dna_client.OutputType.SPLICE_SITES,
                dna_client.OutputType.SPLICE_SITE_USAGE,
                dna_client.OutputType.SPLICE_JUNCTIONS,
            },
            ontology_terms=ontology_terms,
        )
        output.splice_sites.metadata
        longest_transcripts = longest_transcript_extractor.extract(interval)
        # Build plot.
        # Since APOL4 is on the negative DNA strand, we use `filter_negative_strand` to
        # consider only negative stranded splice predictions.
        plot = plot_components.plot(
            [
                plot_components.TranscriptAnnotation(longest_transcripts),
                plot_components.Tracks(
                    tdata=output.splice_sites,
                    ylabel_template='SPLICE SITES: {name} ({strand})',
                ),
            ],
            interval=interval,
            title='Predicted splicing effects for Colon tissue',
        )

    def adjust_interval_with_extra_base(start, stop):
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

