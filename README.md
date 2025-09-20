# Personality Analysis System

A sophisticated trait-based personality analysis tool that helps companies find candidates whose personalities best match specific job descriptions. The system analyzes personality traits using friendliness and dominance scores to create compatibility rankings.

## Features

- **Advanced Trait Management**: Create and manage personality traits with precise friendliness/dominance scores
- **Dynamic Personality Profiling**: Automatically update personality profiles from natural language descriptions
- **Intelligent Company Matching**:
  - Extract personality requirements from job descriptions
  - Calculate compatibility using Euclidean distance algorithms
  - Rank candidates by personality fit with detailed scoring
- **Service-Oriented Architecture**: Clean separation between data access, business logic, and command interfaces
- **Comprehensive CLI**: User-friendly command-line interface with detailed help and validation

## Installation

### Prerequisites
- Python 3.7+
- SQLite3
- pip (Python package manager)

### Setup Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd traits
   ```

2. **Set Up Virtual Environment** (Recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   python setup_dependencies.py
   # Or manually install required packages:
   pip install scipy numpy
   ```

4. **Initialize the System**
   ```bash
   # Set up directories and databases
   python setup_directories.py

   # Populate default traits
   python populate_traits_db.py
   ```

## Usage

### Command Line Interface

The tool provides a comprehensive CLI with the following commands:

#### Trait Operations

```bash
# Create a new personality trait
python main.py trait create <name> <friendliness> <dominance>

# List all available traits
python main.py trait list
```

**Examples:**
```bash
# Create a trait for being detail-oriented
python main.py trait create "detail_oriented" 7.0 5.0

# Create a trait for being creative
python main.py trait create "creative" 8.0 6.0
```

#### Person Operations

```bash
# Create a new person profile
python main.py person create "<full_name>"

# Add personality description to a person
python main.py person add_desc "<name>" "<description>"

# List all person profiles
python main.py person list
```

**Examples:**
```bash
# Create person profiles
python main.py person create "Alice Johnson"
python main.py person create "Bob Smith"

# Add personality descriptions
python main.py person add_desc "Alice Johnson" "friendly, collaborative team player with strong leadership qualities"
python main.py person add_desc "Bob Smith" "analytical, detail-oriented problem solver who works well independently"
```

#### Company Matching

```bash
# Find candidates matching a job description
python main.py company query "<company_name>" "<job_description>"
```

**Examples:**
```bash
# Match for a leadership position
python main.py company query "TechCorp" "seeking innovative leader with strong communication skills"

# Match for a research position
python main.py company query "ResearchLab" "looking for analytical, detail-oriented researcher who can work independently"
```

### Complete Workflow Example

```bash
# 1. Set up some traits
python main.py trait create "innovative" 9.0 8.0
python main.py trait create "analytical" 3.0 4.0
python main.py trait create "collaborative" 8.0 5.0

# 2. Create candidate profiles
python main.py person create "Sarah Chen"
python main.py person create "Mike Rodriguez"
python main.py person create "Emma Davis"

# 3. Add personality descriptions
python main.py person add_desc "Sarah Chen" "innovative and creative problem solver with strong leadership skills"
python main.py person add_desc "Mike Rodriguez" "analytical and detail-oriented researcher who prefers working independently"
python main.py person add_desc "Emma Davis" "collaborative team player who excels in group settings"

# 4. Find matches for different job types
python main.py company query "InnovationTeam" "seeking creative innovators for our R&D department"
python main.py company query "ResearchDept" "looking for independent analytical thinkers"
python main.py company query "MarketingTeam" "need collaborative team players for our creative campaigns"
```

## Project Architecture

### Core Components

- **`main.py`** - CLI entry point with argument parsing and command routing
- **`services/`** - Business logic layer:
  - `person_service.py` - Person-related business operations
  - `company_service.py` - Company matching and analysis logic
- **`person_dao.py`** - Data access object for person database operations
- **`trait_dao.py`** - Data access object for trait database operations
- **`personality_models.py`** - Data classes for personality traits and statistics
- **`db_connection.py`** - Database connection context manager

### Command Modules

- **`trait_commands.py`** - CLI handlers for trait operations
- **`person_commands.py`** - CLI handlers for person operations
- **`company_commands.py`** - CLI handlers for company matching

## Database Schema

### Persons Table
```sql
CREATE TABLE persons (
    person TEXT PRIMARY KEY,
    friendliness REAL DEFAULT 0.0,
    dominance REAL DEFAULT 0.0,
    n_friendliness INTEGER DEFAULT 0,
    n_dominance INTEGER DEFAULT 0
)
```

### Traits Table
```sql
CREATE TABLE traits (
    trait TEXT PRIMARY KEY,
    friendliness REAL,
    dominance REAL
)
```

## Technical Details

### Personality Analysis Algorithm

1. **Trait Extraction**: Natural language descriptions are parsed to identify known personality traits
2. **Weighted Averaging**: Personality scores are calculated using weighted averages, giving more influence to recent traits
3. **Compatibility Scoring**: Euclidean distance between personality vectors determines candidate-job fit
4. **Dynamic Updates**: Personality profiles update automatically as new trait information is added

### Default Traits

The system comes pre-loaded with these personality traits:

- **friendly** (7.0, 6.0) - Warm and approachable
- **helpful** (6.0, 4.0) - Supportive and service-oriented
- **collaborative** (8.0, 5.0) - Team-focused and cooperative
- **outgoing** (9.0, 5.0) - Socially active and extroverted
- **enthusiastic** (8.5, 4.0) - Energetic and positive
- **quiet** (3.0, 2.0) - Reserved and introspective
- **reserved** (2.0, 3.0) - Private and controlled
- **dominant** (6.0, 8.0) - Assertive and commanding
- **assertive** (7.5, 7.5) - Confident and decisive
- **leader** (9.0, 9.0) - Natural leadership qualities
- **strict** (2.0, 8.0) - Firm and uncompromising
- **agile** (8.0, 7.0) - Adaptable and quick-thinking
- **innovative** (9.0, 6.0) - Creative and original

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Database Management
```bash
# Reset and repopulate databases
python populate_db.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For bug reports or feature requests, please open an issue in the project repository.