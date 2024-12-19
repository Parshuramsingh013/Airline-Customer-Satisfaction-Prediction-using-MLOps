from src.logger import get_logger
from src.custome_exception import CustomeException
import sys


logger = get_logger(__name__)

def devide_numbers(a,b):
    try:
        result = a/b
        logger.info("dividing the number")
        return result
    
    except Exception as e:
        logger.error("error occured")
        raise CustomeException("division by zero", sys)
    
if __name__ == "__main__":
    try:
        logger.info("starting main programe ")
        devide_numbers(10,0)
    except CustomeException as ce:
        logger.error(str(ce))
    finally:
        logger.info("end of the programe")


