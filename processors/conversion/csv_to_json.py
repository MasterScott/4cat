"""
Convert a CSV file to JSON
"""
import json

from backend.abstract.processor import BasicProcessor
from backend.lib.exceptions import ProcessorInterruptedException

__author__ = "Stijn Peeters"
__credits__ = ["Stijn Peeters"]
__maintainer__ = "Stijn Peeters"
__email__ = "4cat@oilab.eu"

class ConvertCSVToJSON(BasicProcessor):
	"""
	Convert a CSV file to JSON
	"""
	type = "convert-csv"  # job type ID
	category = "Conversion"  # category
	title = "Convert to JSON"  # title displayed in UI
	description = "Convert a CSV file to JSON"  # description displayed in UI
	extension = "json"  # extension of result file, used internally and in UI

	# all post-processors with CSV output
	accepts = ["search", "collocations", "count-posts", "debate_metrics", "get-entities",
			   "extract-nouns", "hatebase-data", "penelope-semanticframe", "quote-ranker",
			   "tfidf", "thread-metadata", "sentence-split", "hatebase-frequencies",
			   "count-countries", "top-images", "url-extractor", "extract-usernames", "vector-ranker",
			   "count-words", "youtube-metadata", "attribute-frequencies", "count-posts"]

	input = "csv"
	output = "json"

	def process(self):
		"""
		This takes a CSV file as input and writes the same data as a JSON file
		"""
		posts = 0
		self.dataset.update_status("Converting posts")

		# we write to file per row, instead of json.dumps()ing all of it at
		# once, since else we risk having to keep a lot of data in memory,
		# and this buffers one row at most
		with self.dataset.get_results_path().open("w") as output:
			output.write("[")
			for post in self.iterate_items(self.source_file):
				# stop processing if worker has been asked to stop
				if self.interrupted:
					raise ProcessorInterruptedException("Interrupted while processing CSV file")

				posts += 1

				if posts > 1:
					output.write(",")

				output.write(json.dumps(post))
			output.write("]")

		self.dataset.update_status("Finished.")
		self.dataset.finish(num_rows=posts)
