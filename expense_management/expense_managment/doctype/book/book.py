# Copyright (c) 2025, rishabh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from werkzeug.wrappers import Response


class Book(Document):
	pass

@frappe.whitelist()
def new_book():
	"""Create a new book."""
	data = frappe.form_dict
	book = frappe.new_doc("Book")
	book.book_name = data.get("book_name")
	book.author = data.get("author")
	book.insert()

	# return Response(frappe.render_template("templates/includes/Book_List.html"))
	return book_list()

	# return Response("<h1>Book Created Successfully</h1><p>Book Name: {}</p><p>Author: {}</p>".format(
	# 	book.book_name, book.author))

@frappe.whitelist()
def book_list():
	list = frappe.render_template("templates/includes/Book_List.html")
	return Response(list)

@frappe.whitelist(allow_guest=True)
def search_result(search_query):
    books = frappe.db.get_all("Book",
        filters=[["book_name", "like", f"%{search_query}%"], ["author", "like", f"%{search_query}%"]],
        or_filters=True,
        fields=["book_name", "author"]
    )
    return frappe.render_template("templates/includes/search_result.html", {"books": books})
