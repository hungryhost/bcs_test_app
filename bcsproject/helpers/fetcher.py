import datetime
from mainPage.models import Block
import requests


def fetch_blocs(date=datetime.date.today().isoformat()):
	url = 'https://bcschain.info/api/blocks?date={}'.format(date)
	response = requests.get(url)
	blocks = response.json()
	for block in blocks:
		block_to_save = Block(
			hash=block['hash'],
			height=block['height'],
			timestamp=block['timestamp'],
			iso_timestamp=datetime.datetime.utcfromtimestamp(block['timestamp']),
			interval=block['interval'],
			size=block['size'],
			transactionCount=block['transactionCount'],
			miner=block['miner'],
			reward=block['reward'],
		)
		if not Block.objects.filter(hash=block['hash']).exists():
			block_to_save.save()

