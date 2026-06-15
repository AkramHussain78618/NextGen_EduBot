from flask import Flask, render_template, request, jsonify
import requests, re
app=Flask(__name__)
HEADERS={"User-Agent":"NextGenEduBot/2.0"}

TOPIC_MAP={"python":"Python programming language","java":"Java programming language","c":"C programming language","c++":"C++ programming language","dbms":"Database management system","ai":"Artificial intelligence","ml":"Machine learning"}

def normalize(q):
 q=q.strip().lower()
 if q in ["who are you","what is your name","your name"]:
  return None,"I am NextGen EduBot, a student chatbot designed to help with educational topics."
 return TOPIC_MAP.get(q,q),None

def fetch_wikipedia_content(question):
 question,special=normalize(question)
 if special: return special
 try:
  search_url="https://en.wikipedia.org/w/api.php"
  params={"action":"query","list":"search","srsearch":question,"format":"json","srlimit":1}
  r=requests.get(search_url,params=params,headers=HEADERS,timeout=10)
  results=r.json().get("query",{}).get("search",[])
  if not results: return f"I couldn't find information about '{question}'. Please specify the subject clearly."
  title=results[0]["title"]
  s=requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}",headers=HEADERS,timeout=10)
  return s.json().get("extract","No summary available.")
 except requests.exceptions.RequestException:
  return "Network issue occurred. Please try again."
 except Exception:
  return "Sorry, something went wrong."
@app.route("/")
def home(): return render_template("index.html")
@app.route("/chat",methods=["POST"])
def chat():
 q=request.get_json().get("message","")
 return jsonify({"question":q,"answer":fetch_wikipedia_content(q)})
if __name__=="__main__": app.run(debug=True)
