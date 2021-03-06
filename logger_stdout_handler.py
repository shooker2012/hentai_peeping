import logging
import sys

class LoggerStdOutHandler:
    """
    LoggerStdOutHandler's description.
    this class is a fake stream object. It accept a logging.log, and can be set to sys.stdout.After this, the stdout will rediret to the logging.log.
    """
    def __init__( self, logger, log_level = logging.INFO ):
        """__init__
    
        Args: 
            logger: #TODO
            log_level: #TODO

        Returns:
    
        Raises:
        """
    
        self.logger = logger
        self.log_level = log_level
        self.encoding = "utf-8"
    
    def write( self, buffer ):
        """write
    
        Args: 
            buffer: #TODO

        Returns:
    
        Raises:
        """
    
        for line in buffer.rstrip().splitlines():
            line = line.rstrip().encode( 'gbk', "ignore" ).decode( 'gbk', "ignore" )
            self.logger.log(self.log_level, line)

    def flush( self ):
        """flush
    
        Args: None

        Returns:
    
        Raises:
        """
    
        for handler in self.logger.handlers:
            handler.flush( )

    def errors( self ):
        """error
    
        Args: None

        Returns:
    
        Raises:
        """
    
        pass
    
