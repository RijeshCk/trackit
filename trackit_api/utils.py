from django.core.mail import EmailMultiAlternatives
from django.template import loader

def send_confirmation(email,link):
	template_html = 'trackit_api/confirmation_template.html'
	email_context = {'link':link,'email':email}
	subject, from_email, to = 'Password Reset', 'rijesh471@gmail.com', email
	
	html = loader.get_template(template_html)
	html_content = html.render(email_context)
	text_content='This is an important message.'
	# html_content = '<p>This is an <strong>important</strong> message.</p>'
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()
	print "email sent"

def alert_user(email,data):
	template_html = 'trackit_api/alert_confirmation.html'
	email_context = {'email':email,'data':data}
	subject, from_email, to = 'Price Drop Alert', 'rijesh471@gmail.com', email
	
	html = loader.get_template(template_html)
	html_content = html.render(email_context)
	text_content=''
	# html_content = '<p>This is an <strong>important</strong> message.</p>'
	msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()
	print "email sent"