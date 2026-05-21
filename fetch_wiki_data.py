import wikipedia
from wikipedia import RedirectError, PageError, HTTPTimeoutError, DisambiguationError
#The following line is required to avoid a specific bug in the wikipedia loader:
#See also https://forum.langchain.com/t/wikipedialoader-endup-in-jsondecodeerror/3620/2
wikipedia.set_user_agent("research-assistant/0.1 (martin@example.com)")

def fetch_wiki_data(page_title):
    try:
        wikipedia.set_lang("en")
        page = wikipedia.page(page_title, auto_suggest=False)
        return page.content
    except JSONDecodeError as e:
        print("ERROR: Could not fetch wikipedia page",e)
    # wikipedia.exceptions.DisambiguationError(title, may_refer_to)
    # Exception raised when a page resolves to a Disambiguation page.
    # The options property contains a list of titles of Wikipedia pages that the query may refer to.
    except DisambiguationError as e:
        print("ERROR: Page already exists with the same name ",e)
    # exception wikipedia.exceptions.HTTPTimeoutError(query)
    # Exception raised when a request to the Mediawiki servers times out.
    except HTTPTimeoutError as e:
        print("ERROR: Server timed out ",e)

    # exception wikipedia.exceptions.PageError(pageid=None, *args)
    # Exception raised when no Wikipedia matched a query.
    except PageError as e:
        print("ERROR: No Wikipedia page matched the query", e)

    # exception wikipedia.exceptions.RedirectError(title)
    # Exception raised when a page title unexpectedly resolves to a redirect.
    except RedirectError as e:
        print("ERROR: Page title unexpectedly resolves to a redirect", e)
    return ""