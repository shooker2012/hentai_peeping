import logging

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
    
    def write( self, buffer ):
        """write
    
        Args: 
            buffer: #TODO

        Returns:
    
        Raises:
        """
    
        for line in buffer.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush( self ):
        """flush
    
        Args: None

        Returns:
    
        Raises:
        """
    
        for handler in self.logger.handlers:
            handler.flush( )
