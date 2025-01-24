# traits

Personality Analysis System

The Personality Analysis System helps companies find individuals whose personalities match specific job descriptions using trait-based analysis. It calculates personality scores based on friendliness and dominance traits, then ranks candidates by compatibility.

## Features

- **Trait Management**: Store personality traits with friendliness/dominance scores
- **Personality Profiling**: Dynamically update personalities from textual descriptions
- **Company Matching**: 
  - Analyze job descriptions to create target personality profiles
  - Calculate compatibility using Euclidean distance
  - Rank candidates based on personality similarity

## Installation

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**
   ```bash
   python setup_dependencies.py
   ```

3. **Initialize Databases**
   ```bash
   python setup_directories.py
   python populate_traits_db.py  # Loads default traits
   ```

## Usage

### CLI Commands

#### Trait Operations
```bash
# Create new trait
python main.py trait create <name> <friendliness> <dominance>

# List all traits
python main.py trait list

# Example
python main.py trait create punctual 6.0 7.0
```

#### Person Operations
```bash
# Create person
python main.py person create <name>

# Add description to person
python main.py person add_desc <name> "<description>"

# List all persons
python main.py person list

# Example
python main.py person create Alice
python main.py person add_desc Alice "friendly and detail-oriented"
```

#### Company Matching
```bash
# Find candidates matching job description
python main.py company query <company-name> "<job-description>"

# Example
python main.py company query TechStartup "Seeking innovative leaders with strong communication skills"
```

### Example Workflow

1. **Create Person Profile**
   ```bash
   python main.py person create Bob
   python main.py person add_desc Bob "outgoing assertive leader"
   ```

2. **Find Job Matches**
   ```bash
   python main.py company query SalesCorp "We need charismatic team players"
   # Output: Bob - Distance: 1.23
   ```

## Project Structure

Key Components:
- **`company.py`** - Core matching logic and personality analysis
- **`person.py`** - Person profile management
- **`dao/`** - Database access layer:
  - `person_dao.py` - Person database operations
  - `trait_dao.py` - Trait database operations
- **`personality_models.py`** - Data classes for personality traits
- **`company_commands.py`** - CLI command handlers

## Database Schema

**Persons** Table:
- Name | Friendliness | Dominance | Trait Counters

**Traits** Table: 
- Trait Name | Friendliness Score | Dominance Score

## Technical Notes

- Personality scores update dynamically as new traits are added
- Matching uses Euclidean distance between n-dimensional trait vectors
- Default traits include: friendly, dominant, innovative, agile
- Weighted averages ensure recent traits influence scores appropriately

---

For bug reports or feature requests, please open an issue in the project repository.