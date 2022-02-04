import logging
import config

if __name__ == '__main__':
	log = logging.getLogger(__name__)

	cfg = config.Config()
	cfg.save()