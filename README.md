# Gen AI Attendance Portal

A production-ready, full-stack attendance management system built with modern web technologies. This portal provides dual interfaces for students and administrators, featuring real-time analytics, data integrity controls, and automated backup to GitHub.

## Features

### Student Portal
- **Mark Attendance**: Submit attendance with time-sensitive codes
- **View Records**: Access personal attendance history with visual matrix
- **Data Integrity**: Roll number-name locking prevents impersonation
- **Smart Validation**: Duplicate prevention and daily limit enforcement

### Admin Panel
- **Class Management**: Create, configure, and delete classes
- **Attendance Control**: Real-time open/close status management
- **Analytics Dashboard**:
  - Visual insights with pie charts and bar graphs
  - Top/bottom performers tracking
  - Attendance percentage filtering
  - Download attendance matrices as CSV
- **GitHub Integration**: Automatic backup of attendance records
- **Secure Access**: Password-protected admin interface

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit 1.51.0 |
| Database | Supabase (PostgreSQL) |
| Storage | GitHub API |
| Data Processing | Pandas 2.3.3 |
| Visualization | Matplotlib 3.10.7 |
| Language | Python 3.12 |

## Architecture

```
Gen AI Attendance Portal/
├── ATTENDANCE/              # Core application package
│   ├── admin.py            # Admin panel business logic
│   ├── analytics.py        # Analytics dashboard
│   ├── attendance_panel.py # Student attendance viewer
│   ├── student.py          # Student submission logic
│   ├── clients.py          # External service clients
│   ├── config.py           # Configuration management
│   ├── logger.py           # Centralized logging system
│   └── utils.py            # Utility functions
├── logs/                   # Application logs
├── student_main.py         # Student portal entry point
├── admin_main.py           # Admin portal entry point
└── requirements.txt        # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.12
- Supabase account (free tier available)
- GitHub account (optional, for backup feature)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/v6y4k2s/ATTENDANCE-PORTAL.git
   cd ATTENDANCE-PORTAL
   ```

2. **Create virtual environment**

   Using `uv` (recommended):
   ```bash
   uv venv atenv
   source atenv/bin/activate  # On Windows: atenv\Scripts\activate
   ```

   Or using standard Python:
   ```bash
   python3.12 -m venv atenv
   source atenv/bin/activate  # On Windows: atenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Copy the example environment file:
   ```bash
   cp _.envexample .env
   ```

   Edit `.env` with your credentials:
   ```env
   SUPABASE_URL="your_supabase_project_url"
   SUPABASE_KEY="your_supabase_anon_key"
   GITHUB_TOKEN="your_github_personal_access_token"
   GITHUB_USERNAME="your_github_username"
   GITHUB_REPO="your_repo_name"
   ADMIN_USERNAME="your_admin_username"
   ADMIN_PASSWORD="your_admin_password"
   ```

5. **Set up Supabase database**

   Create the following tables in your Supabase project:

   **Table: `classroom_settings`**
   ```sql
   CREATE TABLE classroom_settings (
     class_name TEXT PRIMARY KEY,
     code TEXT NOT NULL,
     daily_limit INTEGER NOT NULL DEFAULT 10,
     is_open BOOLEAN NOT NULL DEFAULT FALSE
   );
   ```

   **Table: `attendance`**
   ```sql
   CREATE TABLE attendance (
     class_name TEXT NOT NULL,
     roll_number INTEGER NOT NULL,
     name TEXT NOT NULL,
     date TEXT NOT NULL,
     PRIMARY KEY (class_name, roll_number, date)
   );
   ```

   **Table: `roll_map`**
   ```sql
   CREATE TABLE roll_map (
     class_name TEXT NOT NULL,
     roll_number INTEGER NOT NULL,
     name TEXT NOT NULL,
     PRIMARY KEY (class_name, roll_number)
   );
   ```

## Usage

### Running the Student Portal

```bash
streamlit run student_main.py
```

**Student Workflow:**
1. Select your class from the dropdown
2. Enter your roll number (numeric only)
3. Enter your name (locked after first submission)
4. Enter the attendance code provided by your instructor
5. Submit attendance
6. View your attendance history in the "View My Attendance" tab

### Running the Admin Portal

```bash
streamlit run admin_main.py
```

**Admin Workflow:**
1. Log in with admin credentials
2. Create new classes via sidebar
3. Select a class to manage
4. Open/close attendance window
5. Set or update attendance code
6. Configure daily limits
7. View attendance matrix and analytics
8. Download reports or push to GitHub

## Key Features Explained

### Roll Map Locking
Once a student submits attendance for the first time with a specific roll number, their name is permanently locked to that roll number. This prevents:
- Identity fraud
- Multiple students using the same roll number
- Name changes mid-semester

### Daily Limit Enforcement
Admins can set a maximum number of students who can mark attendance per day. This helps:
- Prevent overcrowding in physical classrooms
- Enforce capacity constraints
- Manage resource allocation

### Real-time Analytics
The analytics dashboard provides:
- Overall attendance percentage with pie charts
- Top 3 and bottom 3 performers
- Student-wise attendance counts (bar chart)
- Filterable attendance matrix by percentage range

### GitHub Backup
Attendance matrices are automatically pushed to your GitHub repository in the `records/` folder with timestamped filenames:
```
records/attendance_matrix_ClassName_20260214.csv
```

## Engineering Highlights

### Centralized Logging
All operations are logged through a custom logging system (`ATTENDANCE/logger.py`) with:
- Dual output: console + file (`logs/app.log`)
- Detailed formatting with timestamps, module names, and line numbers
- Exception tracking for debugging

### Hierarchical Configuration
Configuration management (`ATTENDANCE/config.py`) supports:
1. Streamlit secrets (for cloud deployment)
2. Environment variables (for local development)
3. Default values (for graceful degradation)

### Multi-layer Error Handling
Every database operation and API call is wrapped with try-except blocks, providing:
- User-friendly error messages
- Detailed exception logging
- Graceful degradation

### Input Validation
- Roll numbers must be numeric
- Attendance codes must match exactly
- Duplicate submissions are prevented
- Daily limits are enforced at database level

## Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy `student_main.py` and `admin_main.py` as separate apps
4. Add your environment variables in the Streamlit Cloud secrets manager

### Local Production

For local production deployment:
```bash
# Run student portal on port 8501
streamlit run student_main.py --server.port 8501

# Run admin portal on port 8502 (in another terminal)
streamlit run admin_main.py --server.port 8502
```

## Security Notes

- Never commit `.env` files to Git (already in `.gitignore`)
- Use strong admin passwords
- Rotate GitHub tokens periodically
- Use Supabase Row Level Security (RLS) for additional protection
- Keep dependencies updated

## Troubleshooting

### Common Issues

**Issue: Supabase connection fails**
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Check if Supabase project is active
- Verify internet connection

**Issue: GitHub push fails**
- Verify `GITHUB_TOKEN` has repo write permissions
- Check if repository exists
- Ensure branch protection rules allow pushes

**Issue: Attendance submission fails**
- Check if classroom is open (`is_open = True`)
- Verify attendance code matches
- Check if daily limit is reached
- Ensure roll number is numeric

### Logs

Check `logs/app.log` for detailed error traces and debugging information.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Enhancements

- [ ] QR code-based attendance
- [ ] Email notifications for admins
- [ ] Attendance photos/selfie verification
- [ ] Bulk student upload (CSV)
- [ ] Export to PDF reports
- [ ] Mobile-responsive design improvements
- [ ] Rate limiting per student
- [ ] Audit logging for admin actions
- [ ] Unit and integration tests

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Built as part of learning journey alongside CS-50 2026
- Inspired by the need for simple, robust attendance systems
- Special thanks to the Streamlit and Supabase communities

## Contact

For questions or support, please open an issue on GitHub.

---

**Built with attention to engineering fundamentals: logging, error handling, configuration management, and clean architecture.**
