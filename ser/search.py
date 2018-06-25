import os
from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, STORED
from whoosh.qparser import MultifieldParser
from jieba.analyse import ChineseAnalyzer


bp = Blueprint('search', __name__)


@bp.route('/search', methods=('GET', 'POST'))
def create():
	if request.method == 'POST':
		keyword = request.form['keyword']
		error = None

		if not keyword:
			error = 'Please input your keyword.'
		
		if error is not None:
			flash(error)
		else:
			results = get_results(keyword, os.path.join(os.getcwd(), 'index'))
			return render_template('result.html', results=results)

	return render_template('search.html')


def get_results(keyword, path):
	analyzer = ChineseAnalyzer()

	schema = Schema(code_id=STORED,
                    name=TEXT(stored=True, analyzer=analyzer),
				    short_intro=TEXT(stored=True, analyzer=analyzer),
					detail_introduce=TEXT(stored=True, analyzer=analyzer),
					type_name=STORED)

	ix = open_dir(path)
	searcher = ix.searcher()
	# parser = QueryParser("content", schema=ix.schema)
	mparser = MultifieldParser(["name", "short_intro", "detail_introduce"],
	                           schema=ix.schema)

	q = mparser.parse(keyword)
	results = searcher.search(q)
	return results