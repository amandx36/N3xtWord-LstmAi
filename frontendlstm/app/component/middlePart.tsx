'use client';

import { useState, useEffect, useRef } from 'react';
import type { FormEvent, ChangeEvent } from 'react';
import './middlepart.css';

type Prediction = {
  word: string;
  probability: number;
};

type PredictionResponse = {
  predictions?: Prediction[];
  error?: string;
  detail?: string;
};

export default function MiddlePart() {
  const[health,setHealth] = useState("")
  const [text, setText] = useState('');
  const [topK, setTopK] = useState(3);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const debounceTimer = useRef<NodeJS.Timeout | null>(null);

  // Auto-predict when user stops typing
  useEffect(() => {
    // Clear previous timer
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current);
    }

    // Don't predict if text is empty
    if (!text.trim()) {
      setPredictions([]);
      setError('');
      return;
    }

    // Set new timer - predict after 800ms of no typing
    debounceTimer.current = setTimeout(() => {
      fetchPredictions(text.trim(), topK);
    }, 800);

    // Cleanup on unmount
    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current);
      }
    };
  }, [text, topK]);

  // function to check the health 
// Function to check backend health
async function checkHealth() {
  setHealth('checking');

  try {
    console.log('Checking backend health...');

    const response = await fetch('/api/health', {
      method: 'GET',
    });

    if (!response.ok) {
      setHealth('offline');
      return;
    }

    setHealth('online');
    console.log('Backend is healthy');
  } catch (problem) {
    console.error('Health check failed:', problem);
    setHealth('offline');
  }
}
// automatically calls when the middle part component mount 
useEffect(() => {
  checkHealth();
}, []);

  async function fetchPredictions(inputText: string, k: number) {
    setError('');
    setIsLoading(true);

    try {
      console.log('Auto-predicting for:', inputText);
      
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText, top_k: k }),
      });
      
      console.log('Response status:', response.status);
      const data: PredictionResponse = await response.json();
      console.log('Response data:', data);

      if (!response.ok) {
        throw new Error(data.error || data.detail || 'The prediction request failed.');
      }
      setPredictions(data.predictions ?? []);
      if (!data.predictions?.length) {
        setError('The model did not return any suggestions for that text.');
      }
    } catch (problem) {
      console.error('Prediction error:', problem);
      setError(problem instanceof Error ? problem.message : 'Something went wrong.');
      setPredictions([]);
    } finally {
      setIsLoading(false);
    }
  }

  function handleTextChange(event: ChangeEvent<HTMLTextAreaElement>) {
    setText(event.target.value);
  }

  function handleWordClick(word: string) {
    // Add the clicked word to the text with a space
    setText(prev => prev.trim() + ' ' + word);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    event.stopPropagation();
    
    if (!text.trim()) {
      setError('Type a sentence first so the model has something to continue.');
      return;
    }

    // Manual prediction trigger
    await fetchPredictions(text.trim(), topK);
  }

  return (
    <section className="predictor" aria-labelledby="predictor-title">
      <div className="predictor-card">
<div className="card-top">
  <span className={`health-status ${health}`}>
    <span className="status-dot"></span>
    {health === 'checking' && 'Checking API...'}
    {health === 'online' && 'API Connected'}
    {health === 'offline' && 'API Disconnected'}
    {health === '' && 'API Status Unknown'}
  </span>

  <div className="eyebrow">
    <span className="status-dot model-dot" />
    LSTM LANGUAGE MODEL
  </div>
</div>
   <h1 id="predictor-title">Your next word,<br /><span>predicted.</span></h1>
        <p className="intro">Give the model a thought. It will suggest a few ways to finish it.</p>

        <form onSubmit={handleSubmit}>
          {/* Predictions shown above the input field */}
          {predictions.length > 0 && (
            <div className="results results-above" aria-live="polite">
              <div className="results-heading"><span>SUGGESTIONS</span><span>CONFIDENCE</span></div>
              {predictions.map((prediction, index) => (
                <div 
                  className="result-row result-row-clickable" 
                  key={`${prediction.word}-${index}`}
                  onClick={() => handleWordClick(prediction.word)}
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => e.key === 'Enter' && handleWordClick(prediction.word)}
                >
                  <span className="result-word">
                    <span className="result-number">0{index + 1}</span>
                    {prediction.word}
                  </span>
                  <span className="result-confidence">{(prediction.probability * 100).toFixed(1)}%</span>
                </div>
              ))}
            </div>
          )}

          {isLoading && (
            <div className="loading-indicator">
              <span className="spinner"></span> Thinking...
            </div>
          )}

          <label className="field-label" htmlFor="userInput">YOUR TEXT</label>
          <textarea
            id="userInput"
            value={text}
            onChange={handleTextChange}
            placeholder="The quick brown fox…"
            maxLength={5000}
            rows={4}
          />
          <div className="form-bottom">
            <label className="top-k-label" htmlFor="topK">Suggestions
              <select id="topK" value={topK} onChange={(event) => setTopK(Number(event.target.value))}>
                {[3, 5, 7, 10].map((count) => <option key={count} value={count}>{count}</option>)}
              </select>
            </label>
            <span className="character-count">{text.length}/5000</span>
          </div>
          <button className="predict-button" type="submit" disabled={isLoading || !text.trim()}>
            {isLoading ? 'Thinking…' : 'Predict now'}
            <span aria-hidden="true">↗</span>
          </button>
        </form>

        {error && <p className="message error-message" role="alert">{error}</p>}

        <div className="card-note"><span aria-hidden="true">✦</span> Type and pause - predictions appear automatically. Click a word to add it.</div>
      </div>
    </section>
  );
}
