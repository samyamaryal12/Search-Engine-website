import os
import json

class StorySearchEngine:
    def __init__(self, dataset_dir, image_map_file):
        self.dataset_dir = dataset_dir
        self.image_map = self._load_image_map(image_map_file)
        self.indexed_stories = self._index_stories()

    def _load_image_map(self, image_map_file):
        with open(image_map_file, 'r') as f:
            return json.load(f)

    def _index_stories(self):
        stories = []
        for file in os.listdir(self.dataset_dir):
            if file.endswith('.txt'):
                with open(os.path.join(self.dataset_dir, file), 'r', encoding='utf-8') as f:
                    title = file.replace('.txt', '').replace('_', ' ')
                    content = f.read()
                    image_url = self.image_map.get(file.replace('.txt', ''), 'https://upload.wikimedia.org/wikipedia/commons/a/a3/Image-not-found.png')
                    stories.append({
                        'title': title,
                        'content': content,
                        'image': image_url
                    })
        print(f"Indexed {len(stories)} stories.")
        return stories

    def search(self, query):
        query = query.lower()
        
        # Boolean logic: Handle AND, OR, NOT
        if " and " in query:
            terms = query.split(" and ")
            results = self._handle_and(terms)
        elif " or " in query:
            terms = query.split(" or ")
            results = self._handle_or(terms)
        elif " not " in query:
            terms = query.split(" not ")
            results = self._handle_not(terms)
        else:
            # Simple search without boolean operators
            results = self._simple_search(query)
        
        print(f"Found {len(results)} results for query '{query}'.")
        return results

    def _simple_search(self, query):
        results = []
        for story in self.indexed_stories:
            if query in story['title'].lower() or query in story['content'].lower():
                results.append(story)
        return results

    def _handle_and(self, terms):
        term1, term2 = terms[0].strip(), terms[1].strip()
        results = []
        for story in self.indexed_stories:
            if (term1 in story['title'].lower() or term1 in story['content'].lower()) and \
               (term2 in story['title'].lower() or term2 in story['content'].lower()):
                results.append(story)
        return results

    def _handle_or(self, terms):
        term1, term2 = terms[0].strip(), terms[1].strip()
        results = []
        for story in self.indexed_stories:
            if term1 in story['title'].lower() or term1 in story['content'].lower() or \
               term2 in story['title'].lower() or term2 in story['content'].lower():
                results.append(story)
        return results

    def _handle_not(self, terms):
        term1, term2 = terms[0].strip(), terms[1].strip()
        results = []
        for story in self.indexed_stories:
            if (term1 in story['title'].lower() or term1 in story['content'].lower()) and \
               term2 not in story['title'].lower() and term2 not in story['content'].lower():
                results.append(story)
        return results