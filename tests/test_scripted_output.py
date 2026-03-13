import pytest
import pandas as pd
import numpy as np
from src.analyzers import (
    PublicationTrendAnalyzer,
    AuthorsAnalyzer,
    LanguageAnalyzer,
    PublisherAnalyzer,
    MissingISBNAnalyzer,
    LanguageYearAnalyzer
)

@pytest.fixture
def sample_data():
    """Create a sample DataFrame for testing analyzers."""
    data = {
        'book': ['B1', 'B2', 'B3', 'B4', 'B5', 'B6'],
        'author': ['A1', 'A1', 'A2', 'A3', 'A1', 'A2'],
        'publication date': ['2000', '2001', '2000', '1999', '2020', 'invalid'],
        'language': ['eng', 'eng', 'fra', 'eng', 'deu', 'eng'],
        'book publisher': ['P1', 'P1', 'P2', 'P3', 'P4', 'P5'],
        'isbn': ['123', None, '456', float('nan'), '789', '']
    }
    df = pd.DataFrame(data)
    # Simulate loading causing NaN for None/NaN inputs
    return df

class TestPublicationTrendAnalyzer:
    def test_analyze(self, sample_data):
        analyzer = PublicationTrendAnalyzer()
        result = analyzer.analyze(sample_data)
        
        # Check years: 1999, 2000 (occurrs twice), 2001, 2020. 'invalid' is dropped.
        counts = result['counts']
        assert counts.loc[2000] == 2
        assert counts.loc[1999] == 1
        assert 1999 in counts.index
        assert 2020 in counts.index
        
        # Check trend line exists
        assert result['trend_line'] is not None
        assert 'slope' in result['trend_line']

class TestAuthorsAnalyzer:
    def test_analyze(self, sample_data):
        analyzer = AuthorsAnalyzer()
        result = analyzer.analyze(sample_data)
        
        # A1 has 3 books, A2 has 2, A3 has 1
        assert result['A1'] == 3
        assert result['A2'] == 2
        assert len(result) <= 5

class TestLanguageAnalyzer:
    def test_analyze(self, sample_data):
        analyzer = LanguageAnalyzer()
        result = analyzer.analyze(sample_data)
        
        # eng: 4, fra: 1, deu: 1
        assert result['eng'] == 4
        assert result['fra'] == 1
        assert result['deu'] == 1

class TestPublisherAnalyzer:
    def test_analyze(self, sample_data):
        analyzer = PublisherAnalyzer()
        
        # Create larger dataset to trigger "Others" logic (need > 20 publishers)
        # We reuse the analyzer logic but mock data specifically for this test
        large_data = pd.DataFrame({
            'book publisher': [f'Pub{i}' for i in range(25)] + ['Pub0', 'Pub0']
        })
        
        result = analyzer.analyze(large_data)
        
        # Should return a dict with counts and others_details
        assert isinstance(result, dict)
        assert 'counts' in result
        assert 'Others' in result['counts']
        assert result['counts']['Pub0'] == 3  # 1 original + 2 added
        
        # Test small data
        result_small = analyzer.analyze(sample_data)
        # Should just be a series
        assert isinstance(result_small, pd.Series)
        assert result_small['P1'] == 2

class TestMissingISBNAnalyzer:
    def test_analyze(self, sample_data):
        analyzer = MissingISBNAnalyzer()
        result = analyzer.analyze(sample_data)
        
        # Total 6 records
        # Missing: None, float('nan'), maybe '' depending on pandas read.
        # In our fixture: None and float('nan') are definitely NaN. '' is empty string.
        # Analyzer checks .isna().sum(). Empty string might not be NaN by default unless converted.
        # Let's adjust expectation based on typical pandas behavior or analyzer logic.
        # Analyzer code: missing_count = data['isbn'].isna().sum()
        
        # In sample_data: None -> NaN, float('nan') -> NaN. '' -> string.
        # So expected missing is 2.
        
        assert result['total'] == 6
        assert result['missing'] == 2
        assert result['percentage'] == round(2/6 * 100, 2)

class TestLanguageYearAnalyzer:
    def test_analyze(self, sample_data):
        analyzer = LanguageYearAnalyzer()
        result = analyzer.analyze(sample_data)
        
        # Columns should be languages, Index should be years
        assert 'eng' in result.columns
        assert 2000 in result.index
        
        # Check specific intersection
        # Year 2000: B1(eng), B3(fra) -> eng=1, fra=1
        assert result.at[2000, 'eng'] == 1
        assert result.at[2000, 'fra'] == 1
        assert result.at[2000, 'deu'] == 0

if __name__ == "__main__":
    pytest.main([__file__])
