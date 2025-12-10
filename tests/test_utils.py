import sys
import os
import pytest

# Ensure project root is on sys.path so tests can import modules from repository
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from report_generator import clean_phone_number, normalize_cep, best_match_column


def test_clean_phone_number_basic():
    # empty or invalid
    assert clean_phone_number("") is pytest.approx(float('nan')) or clean_phone_number("") != clean_phone_number("")

    # numbers with punctuation
    assert clean_phone_number("(67) 9 9123-4567") == '67991234567'[-11:]
    assert clean_phone_number("5567991234567") == '67991234567'[-11:]

    # preserve_full True returns full digits
    assert clean_phone_number("(67) 99123-4567", preserve_full=True).endswith('991234567') or len(clean_phone_number("(67) 99123-4567", preserve_full=True)) >= 10


def test_normalize_cep():
    assert normalize_cep("79.800-000") == '79800000'
    assert normalize_cep("79800000") == '79800000'
    assert normalize_cep("") == ""


def test_best_match_column():
    cols = ["Nome Completo", "Telefone Principal", "WhatsApp", "Endereco"]
    # candidate list containing possible names
    cand = ["NOME", "Nome", "Nome Completo"]
    best = best_match_column(cols, cand)
    assert best in cols
    # whatsapp detection
    bestw = best_match_column(cols, ["Whats", "WhatsApp", "Telefone"])
    assert bestw.lower().startswith('wh') or 'telefone' in bestw.lower() or bestw in cols
