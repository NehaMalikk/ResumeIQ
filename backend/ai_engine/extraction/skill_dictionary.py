"""Built-in technical skill vocabulary used by the deterministic extractor."""

from __future__ import annotations

from collections.abc import Mapping


# Canonical names are deliberately kept separate from matching aliases so this
# vocabulary can be extended without changing extraction logic.
SKILL_CATEGORIES: Mapping[str, str] = {
    "Python": "Programming Language", "Java": "Programming Language", "JavaScript": "Programming Language", "TypeScript": "Programming Language", "C": "Programming Language", "C++": "Programming Language", "C#": "Programming Language", "Go": "Programming Language", "Rust": "Programming Language", "PHP": "Programming Language", "Ruby": "Programming Language", "Kotlin": "Programming Language", "Swift": "Programming Language", "Scala": "Programming Language", "R": "Programming Language", "SQL": "Programming Language", "Bash": "Programming Language", "PowerShell": "Programming Language", "Dart": "Programming Language",
    "FastAPI": "Framework", "Flask": "Framework", "Django": "Framework", "React": "Framework", "Next.js": "Framework", "Angular": "Framework", "Vue.js": "Framework", "Node.js": "Framework", "Express": "Framework", "Spring Boot": "Framework", ".NET": "Framework", "Laravel": "Framework", "Ruby on Rails": "Framework", "ASP.NET": "Framework", "Svelte": "Framework", "React Native": "Mobile Development",
    "TensorFlow": "Machine Learning", "PyTorch": "Machine Learning", "Scikit-Learn": "Machine Learning", "Keras": "Machine Learning", "XGBoost": "Machine Learning", "Pandas": "Data Science", "NumPy": "Data Science", "SciPy": "Data Science", "Matplotlib": "Data Science", "Seaborn": "Data Science", "OpenCV": "Computer Vision", "Hugging Face": "AI",
    "PostgreSQL": "Database", "MySQL": "Database", "SQLite": "Database", "MongoDB": "Database", "Redis": "Database", "Elasticsearch": "Database", "Oracle": "Database", "Microsoft SQL Server": "Database", "Cassandra": "Database", "DynamoDB": "Database", "Firebase": "Database", "Snowflake": "Data Engineering",
    "AWS": "Cloud", "Azure": "Cloud", "GCP": "Cloud", "Docker": "DevOps", "Kubernetes": "DevOps", "Terraform": "DevOps", "Ansible": "DevOps", "Jenkins": "DevOps", "GitHub Actions": "DevOps", "GitLab CI": "DevOps", "CircleCI": "DevOps", "Linux": "Operating System", "Windows": "Operating System", "macOS": "Operating System", "Nginx": "DevOps", "Apache": "DevOps",
    "Git": "Version Control", "GitHub": "Version Control", "GitLab": "Version Control", "Bitbucket": "Version Control", "Jira": "Project Management", "REST API": "API", "GraphQL": "API", "Kafka": "Data Engineering", "Apache Spark": "Data Engineering", "Airflow": "Data Engineering", "ETL": "Data Engineering", "Pytest": "Testing", "JUnit": "Testing", "Selenium": "Testing", "Cypress": "Testing", "Postman": "Testing",
    "OAuth": "Cyber Security", "JWT": "Cyber Security", "OWASP": "Cyber Security", "Burp Suite": "Cyber Security", "Kali Linux": "Cyber Security", "Android": "Mobile Development", "iOS": "Mobile Development", "Flutter": "Mobile Development", "SwiftUI": "Mobile Development",
}

SKILL_ALIASES: Mapping[str, str] = {
    "py": "Python", "python3": "Python", "js": "JavaScript", "ts": "TypeScript", "nodejs": "Node.js", "node js": "Node.js", "reactjs": "React", "react js": "React", "nextjs": "Next.js", "next js": "Next.js", "vuejs": "Vue.js", "vue js": "Vue.js", "postgres": "PostgreSQL", "mssql": "Microsoft SQL Server", "ms sql server": "Microsoft SQL Server", "github": "GitHub", "aws cloud": "AWS", "google cloud": "GCP", "google cloud platform": "GCP", "g cloud": "GCP", "scikit learn": "Scikit-Learn", "sklearn": "Scikit-Learn", "tf": "TensorFlow", "k8s": "Kubernetes", "dotnet": ".NET", "dot net": ".NET", "asp net": "ASP.NET", "c sharp": "C#", "cplusplus": "C++", "c plus plus": "C++",
}
