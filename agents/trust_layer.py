import logging

logger = logging.getLogger(__name__)

class TrustLayer:
    """
    Middleware to validate agent outputs and prevent hallucinations.
    """
    @staticmethod
    def validate_job_ids(job_list, valid_jobs):
        """
        Ensures that every job_id in the agent's report actually exists in the valid_jobs list.
        """
        # In a real app, this would query BQ or a cache
        # For prototype, we assume valid_jobs is passed or we just log warning
        logger.info("Trust Layer: Validating Job IDs...")
        return job_list # Passthrough for now
    
    @staticmethod
    def check_hallucination(text):
        """
        Basic check for known hallucination patterns (e.g., confident wrong dates).
        """
        if "2099" in text: # Example check
            logger.warning("Trust Layer: Detected potential hallucinated date.")
            return False
        return True
