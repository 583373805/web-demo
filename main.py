import cherrypy
import os.path
import function_tools as tool


class DataTrackWeb(object):

    @cherrypy.expose
    def index(self):
        return open('html/index.html', encoding='UTF-8')


@cherrypy.expose()
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class CloudStackTrackWebService(object):

    def GET(self, category, item):
        data = tool.select(category, item)
        return data

    def POST(self):
        request_data = cherrypy.request.json
        category = request_data.get('category')
        item = request_data.get("item")
        tool.update(category, item)

    def PUT(self):
        request_data = cherrypy.request.json
        category = request_data.get('category')
        item = request_data.get("item")
        tool.insert(category, item)

    def DELETE(self, category, item):
        tool.delete(category, item)


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/cs': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Context-Type', 'application/json')]
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '.'
        }
    }
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8090
    })
    webapp = DataTrackWeb()
    webapp.cs = CloudStackTrackWebService()
    cherrypy.quickstart(webapp, '/', conf)
