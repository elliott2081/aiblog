from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Featured/recent posts for home page
    recent_posts = [
        {
            'title': 'About Me and My AI Journey',
            'slug': 'about-me',
            'excerpt': 'Software Developer with 10 years experience documenting AI discoveries and experiments.',
            'date': '2025-05-27'
        }
    ]
    return render_template('index.html', posts=recent_posts)

@app.route('/post/<slug>')
def post(slug):
    # For now, just handle the about-me post
    if slug == 'about-me':
        post_data = {
            'title': 'About Me and My AI Journey',
            'date': '2025-05-27',
            'content': '''
            <p>Hello! I'm a Software Developer with 10 years of experience in Web Development. Currently, I work as an SDET (Software Development Engineer in Test) at an AAC (Augmentative and Alternative Communication) Device company, where I help ensure that communication technology works seamlessly for those who need it most.</p>
            
            <h2>What Drives Me</h2>
            <p>I have a passion for automating processes and discovering new AI tools that can make development more efficient and enjoyable. There's something deeply satisfying about turning repetitive tasks into elegant, automated solutions.</p>
            
            <h2>Why This Blog?</h2>
            <p>This blog is an effort to document what I find and experiment with in the rapidly evolving world of AI. I believe in learning by doing, and I want to share that journey with others who are equally curious about the intersection of traditional software development and cutting-edge AI capabilities.</p>
            
            <h2>What to Expect</h2>
            <p>I hope this space will soon be filled with:</p>
            <ul>
                <li><strong>Interesting Projects</strong> - Real-world applications of AI in development workflows</li>
                <li><strong>Games & Interactive Experiments</strong> - Because learning should be fun</li>
                <li><strong>AI Tool Reviews</strong> - Honest takes on what works (and what doesn't)</li>
                <li><strong>Automation Adventures</strong> - Stories from the trenches of process improvement</li>
            </ul>
            
            <p>Whether you're a fellow developer, an AI enthusiast, or just someone curious about where technology is heading, I hope you'll find something valuable here. Let's explore this brave new world of AI-assisted development together!</p>
            '''
        }
        return render_template('post.html', post=post_data)
    else:
        return "Post not found", 404

@app.route('/projects')
def projects():
    # Simple list of projects for now
    project_list = [
        {
            'name': 'Campground Backend',
            'description': 'API for collecting campground data from various sources',
            'tech': 'Node.js, Express'
        },
        {
            'name': 'Dave Website',
            'description': 'Personal website with 3D resume',
            'tech': 'Next.js, TypeScript'
        },
        {
            'name': 'JS Games',
            'description': 'Collection of browser-based games including Pac-Man',
            'tech': 'JavaScript, Phaser'
        }
    ]
    return render_template('projects.html', projects=project_list)

if __name__ == '__main__':
    app.run(debug=True, port=9000)