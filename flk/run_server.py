# -*- coding:utf-8 -*-
from flk import app
if __name__ == "__main__":
    print app.url_map
    app.run(debug=True, host='localhost', port=9100)
