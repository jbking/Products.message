from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from zope.interface import Interface, implements
from zope import schema
from five import grok


class IMessage(Interface):
    """An email-like message
    """

    subject = schema.TextLine(title=u"Subject")
    body = schema.Text(title=u"Body", required=False)


class Message(SimpleItem):
    implements(IMessage)

    meta_type = 'Message'

    subject = u""
    body = u""

    def __init__(self, id, subject, body):
        self.id = id
        self.subject = subject
        self.body = body


class MessageView(grok.View):

    grok.context(IMessage)
    grok.require('zope2.View')
    grok.name('index_html')

    def update(self):
        self.message = IMessage(self.context)

    def render(self):
        return "subject: %s, body: %s" % (
            self.message.subject, self.message.body)


def addForm(_):
    """Returns an HTML form."""
    return """<html>
    <head><title>Add Message</title></head>
    <body>
    <form action="addFunction">
    id <input type="type" name="id"><br>
    subject <input type="type" name="subject"><br>
    <textarea name="body:lines"></textarea>
    <input type="submit">
    </form>
    </body>
    </html>"""


def addFunction(dispatcher, id, subject, body):
    """Create a message."""
    m = Message(id, subject, body)
    dispatcher.Destination()._setObject(id, m)
    dispatcher.manage_main(dispatcher, dispatcher.REQUEST)


def initialize(registrar):
    InitializeClass(Message)
    registrar.registerClass(
        Message,
        constructors=(addForm, addFunction))
