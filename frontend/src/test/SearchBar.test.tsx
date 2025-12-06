/**
 * Tests for SearchBar component
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { SearchBar } from '../components/SearchBar';

describe('SearchBar', () => {
  it('renders with placeholder', () => {
    render(<SearchBar value="" onChange={vi.fn()} />);
    
    const input = screen.getByPlaceholderText(/search by customer name or phone/i);
    expect(input).toBeInTheDocument();
  });

  it('displays initial value', () => {
    render(<SearchBar value="test query" onChange={vi.fn()} />);
    
    const input = screen.getByDisplayValue('test query');
    expect(input).toBeInTheDocument();
  });

  it('calls onChange after debounce', async () => {
    const onChange = vi.fn();
    render(<SearchBar value="" onChange={onChange} />);
    
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'new search' } });
    
    // Should not call immediately
    expect(onChange).not.toHaveBeenCalled();
    
    // Should call after debounce (300ms)
    await waitFor(() => expect(onChange).toHaveBeenCalledWith('new search'), {
      timeout: 500,
    });
  });

  it('shows clear button when value exists', () => {
    render(<SearchBar value="test" onChange={vi.fn()} />);
    
    const clearButton = screen.getByLabelText(/clear search/i);
    expect(clearButton).toBeInTheDocument();
  });

  it('clears input when clear button clicked', async () => {
    const onChange = vi.fn();
    render(<SearchBar value="test" onChange={onChange} />);
    
    const clearButton = screen.getByLabelText(/clear search/i);
    fireEvent.click(clearButton);
    
    await waitFor(() => expect(onChange).toHaveBeenCalledWith(''));
  });
});
