import webbrowser

def web_search(query, gui_instance=None):
    query = query.replace(" ", "+")  
    url = f"https://www.google.com/search?q={query}" 
    webbrowser.open(url)

    response_text = f"Search for results {query} in google"
    
    gui_instance.ai_response_received.emit(response_text)