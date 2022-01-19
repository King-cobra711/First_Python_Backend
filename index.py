import tornado.web
import tornado.ioloop
import json

class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World! This is a python command executed from the backend")
class listRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
class queryParamRequestHandler(tornado.web.RequestHandler):
    def get(self):
        num = self.get_argument("num")
        if(num.isdigit()):
            r = "odd" if int(num) % 2 else "even"
            self.write(f"The integer {num} is {r}")
        else:
            self.write(f"{num} is not a valid integer.")
class resourceParamRequestHandler(tornado.web.RequestHandler):
    def get(self, studentName, courseID):
        match courseID:
            case "1":
                subject = "Biology"
            case "2":
                subject = "Physics"
            case "3":
                subject = "Sports Science"
            case "4":
                subject = "English"
            case _:
                subject = ""
        if subject == "":
            self.write(f"Sorry {studentName}, course ID {courseID} does not relate to any subject")
        else:
            self.write(f"Hello {studentName}, Welcom to {subject} class!")
class fruitRequestHandler(tornado.web.RequestHandler):
    def get(self):
        fh = open("list.txt", "r")
        fruits = fh.read().splitlines()
        fh.close()
        self.write(json.dumps(fruits))
    def post(self):
        fruit = self.get_argument("fruit")
        fh = open("list.txt", "a")
        fh.write(f"{fruit}\n")
        fh.close
        self.write(json.dumps({f"message": "Your fruit has been added to the list!"}))
class uploadImageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("image.html")
    def post(self):
        files = self.request.files["imgFile"]
        for f in files:
            fh = open(f"images/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
        self.write(f'<a href="http://localhost:3001/img/{f.filename}">{f.filename}</a>')
        #There is a limit to the file size you can upload. Approx 1-2mb 
    
class mainRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", basicRequestHandler),
        (r"/animal", listRequestHandler),
        (r"/isEven", queryParamRequestHandler),
        (r"/students/([a-z]+)/([0-9]+)", resourceParamRequestHandler),
        (r"/fruits", fruitRequestHandler),
        (r"/main", mainRequestHandler),
        (r"/uploadimage", uploadImageHandler),
        (r"/img.(.*)", tornado.web.StaticFileHandler, {"path": "./images"})
        #regex101.com
    ])



port = 3001
app.listen(port)
print(f"Listening on port: {port}")
tornado.ioloop.IOLoop.current().start()