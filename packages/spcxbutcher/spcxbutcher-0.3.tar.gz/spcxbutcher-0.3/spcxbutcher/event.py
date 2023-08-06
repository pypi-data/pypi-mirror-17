import logging

class InvalidEventRecord( Exception ):
    pass

class Event:
    def __init__( self, rawData, hightime ):
        self.type = 'event'
        timestamp = rawData & 0x00ffffff
        self.lvttl = self._lvttl( rawData )
        self.gap = rawData >> 29
        self.timestamp = hightime + timestamp

    def __repr__( self ):
        return str( ( self.lvttl, self.timestamp, self.gap ) )

    @classmethod
    def verifyEventRecordHeader( self, rawData ):
        highestTwoBits = ( rawData & 0xc0000000 ) >> 30
        if highestTwoBits not in [ 0b00, 0b01 ]:
            raise InvalidEventRecord( 'invalid rawData record: {:08x}'.format( rawData ) )

    @property
    def channel( self ):
        return self.lvttl

    def _lvttl( self, event ):
        channel = ( event >> 24 ) & 0b00011111
        if channel < 3 or channel > 14:
            raise Exception( "unexpected channel value: {}".format( channel ) )
        if channel <= 10:
            return channel - 2
        else:
            return channel - 4

    def __eq__( self, _tuple ):
        return ( self.lvttl, self.timestamp, self.gap ) == _tuple
