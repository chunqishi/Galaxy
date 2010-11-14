"""
Provides utilities for working with GFF files.
"""

from bx.intervals.io import *

class GFFInterval( GenomicInterval ):
    """ 
    A GFF interval, including attributes. If file is strictly a GFF file,
    only attribute is 'group.'
    """
    def __init__( self, reader, fields, chrom_col, start_col, end_col, strand_col, default_strand, \
                  fix_strand=False, raw_line='' ):
        GenomicInterval.__init__( self, reader, fields, chrom_col, start_col, end_col, strand_col, \
                                  default_strand, fix_strand=fix_strand )
        self.raw_line = raw_line
        self.attributes = parse_gff_attributes( fields[8] )
                
class GFFFeature( GenomicInterval ):
    """
    A GFF feature, which can include multiple intervals.
    """
    def __init__( self, reader, chrom_col, start_col, end_col, strand_col, default_strand, \
                  fix_strand=False, intervals=[] ):
        GenomicInterval.__init__( self, reader, intervals[0].fields, chrom_col, start_col, end_col, \
                                  strand_col, default_strand, fix_strand=fix_strand )
        self.intervals = intervals
        # Use intervals to set feature attributes.
        for interval in self.intervals:
            # Error checking.
            if interval.chrom != self.chrom:
                raise ValueError( "interval chrom does not match self chrom: %i != %i" % \
                                  ( interval.chrom, self.chrom ) )
            if interval.strand != self.strand:
                raise ValueError( "interval strand does not match self strand: %s != %s" % \
                                  ( interval.strand, self.strand ) )
            # Set start, end of interval.
            if interval.start < self.start:
                self.start = interval.start
            if interval.end > self.end:
                self.end = interval.end
                
class GFFIntervalToBEDReaderWrapper( NiceReaderWrapper ):
    """ 
    Reader wrapper that reads GFF intervals/lines and automatically converts
    them to BED format. 
    """
    
    def parse_row( self, line ):
        # HACK: this should return a GFF interval, but bx-python operations 
        # require GenomicInterval objects and subclasses will not work.
        interval = GenomicInterval( self, line.split( "\t" ), self.chrom_col, self.start_col, \
                                    self.end_col, self.strand_col, self.default_strand, \
                                    fix_strand=self.fix_strand )
        interval = convert_gff_coords_to_bed( interval )
        return interval

class GFFReaderWrapper( NiceReaderWrapper ):
    """
    Reader wrapper for GFF files.
    
    Wrapper has two major functions:
    (1) group entries for GFF file (via group column), GFF3 (via id attribute ), 
        or GTF (via gene_id/transcript id);
    (2) convert coordinates from GFF format--starting and ending coordinates 
        are 1-based, closed--to the 'traditional'/BED interval format--0 based, 
        half-open. This is useful when using GFF files as inputs to tools that 
        expect traditional interval format.
    """
    
    def __init__( self, reader, **kwargs ):
        """
        Create wrapper. Defaults are group_entries=False and 
        convert_coords_to_bed=True to support backward compatibility.
        """
        NiceReaderWrapper.__init__( self, reader, **kwargs )
        self.group_entries = kwargs.get( 'group_entries', False )
        self.convert_coords_to_bed = kwargs.get( 'convert_coords_to_bed', True )
        self.last_line = None
        self.cur_offset = 0
        self.seed_interval = None
    
    def parse_row( self, line ):
        interval = GFFInterval( self, line.split( "\t" ), self.chrom_col, self.start_col, \
                                self.end_col, self.strand_col, self.default_strand, \
                                fix_strand=self.fix_strand, raw_line=line )
        if self.convert_coords_to_bed:
            interval = convert_gff_coords_to_bed( interval )
        return interval
        
    def next( self ):
        """ Returns next GFFFeature. """
        
        #
        # Helper function.
        #
        
        def handle_parse_error( parse_error ):
            """ Actions to take when ParseError found. """
            if self.outstream:
               if self.print_delegate and hasattr(self.print_delegate,"__call__"):
                   self.print_delegate( self.outstream, e, self )
            self.skipped += 1
            # no reason to stuff an entire bad file into memmory
            if self.skipped < 10:
               self.skipped_lines.append( ( self.linenum, self.current_line, str( e ) ) )
               
        #
        # Get next GFFFeature
        # 

        # If there is no seed interval, set one. Also, if there are no more 
        # intervals to read, this is where iterator dies.
        if not self.seed_interval:
            while not self.seed_interval:
                try:
                    self.seed_interval = GenomicIntervalReader.next( self )
                except ParseError, e:
                    handle_parse_error( e )
    
        # Initialize feature name from seed.
        feature_group = self.seed_interval.attributes.get( 'group', None ) # For GFF
        feature_id = self.seed_interval.attributes.get( 'id', None ) # For GFF3
        feature_gene_id = self.seed_interval.attributes.get( 'gene_id', None ) # For GTF
        feature_transcript_id = self.seed_interval.attributes.get( 'transcript_id', None ) # For GTF

        # Read all intervals associated with seed.
        feature_intervals = []
        feature_intervals.append( self.seed_interval )
        while True:
            try:
                interval = GenomicIntervalReader.next( self )
            except StopIteration, e:
                # No more intervals to read, but last feature needs to be 
                # returned.
                interval = None
                break
            except ParseError, e:
                handle_parse_error( e )
            
            # If interval not associated with feature, break.
            group = interval.attributes.get( 'group', None )
            if group and feature_group != group:
                break
            id = interval.attributes.get( 'id', None )
            if id and feature_id != id:
                break
            gene_id = interval.attributes.get( 'gene_id', None )
            transcript_id = interval.attributes.get( 'transcript_id', None )
            if transcript_id and transcript_id != feature_transcript_id and gene_id and \
               gene_id != feature_gene_id:
                break
    
            # Interval associated with feature.
            feature_intervals.append( interval )
   
        # Last interval read is the seed for the next interval.
        self.seed_interval = interval
    
        # Return GFF feature with all intervals.    
        return GFFFeature( self, self.chrom_col, self.start_col, self.end_col, self.strand_col, \
                           self.default_strand, fix_strand=self.fix_strand, \
                           intervals=feature_intervals )
        

def convert_bed_coords_to_gff( interval ):
    """
    Converts an interval object's coordinates from BED format to GFF format. 
    Accepted object types include GenomicInterval and list (where the first 
    element in the list is the interval's start, and the second element is 
    the interval's end).
    """
    if type( interval ) is GenomicInterval:
        interval.start += 1
    elif type ( interval ) is list:
        interval[ 0 ] += 1
    return interval
    
def convert_gff_coords_to_bed( interval ):
    """
    Converts an interval object's coordinates from GFF format to BED format. 
    Accepted object types include GenomicInterval and list (where the first
    element in the list is the interval's start, and the second element is 
    the interval's end).
    """
    if type( interval ) is GenomicInterval:
        interval.start -= 1
    elif type ( interval ) is list:
        interval[ 0 ] -= 1
    return interval
    
def parse_gff_attributes( attr_str ):
    """
    Parses a GFF/GTF attribute string and returns a dictionary of name-value 
    pairs. The general format for a GFF3 attributes string is 
        name1=value1;name2=value2
    The general format for a GTF attribute string is 
        name1 "value1" ; name2 "value2"
    The general format for a GFF attribute string is a single string that
    denotes the interval's group; in this case, method returns a dictionary 
    with a single key-value pair, and key name is 'group'
    """    
    attributes_list = attr_str.split(";")
    attributes = {}
    for name_value_pair in attributes_list:
        # Try splitting by space and, if necessary, by '=' sign.
        pair = name_value_pair.strip().split(" ")
        if len( pair ) == 1:
            pair = name_value_pair.strip().split("=")
        if len( pair ) == 1:
            # Could not split for some reason -- raise exception?
            continue
        if pair == '':
            continue
        name = pair[0].strip()
        if name == '':
            continue
        # Need to strip double quote from values
        value = pair[1].strip(" \"")
        attributes[ name ] = value
        
    if len( attributes ) == 0:
        # Could not split attributes string, so entire string must be 
        # 'group' attribute. This is the case for strictly GFF files.
        attributes['group'] = attr_str
    return attributes