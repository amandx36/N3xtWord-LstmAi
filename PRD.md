# NextWord AI
## Product Requirements Document (PRD)

**Version:** 1.0  
**Product Type:** AI-powered web application  
**Primary Goal:** Predict the next word in a text sequence using a custom-trained LSTM model.

---

## 1. Product Overview

NextWord AI is a web application that predicts the most likely next word based on the text entered by a user.

The application uses a custom LSTM model trained on the WikiText-103 dataset. Users can enter text, receive next-word predictions, explore alternative suggestions, and experiment with different input contexts.

The product combines deep learning, backend API development, and modern frontend engineering into a deployable full-stack application.

### Vision

Build an interactive, responsive, and technically transparent next-word prediction application that demonstrates practical knowledge of deep learning and full-stack development.

---

## 2. Problem Statement

Typing assistants and predictive text systems help users write faster by suggesting likely next words.

This project explores how a recurrent neural network can learn sequential language patterns and use previous tokens to predict the next token.

The application will provide an interactive interface for testing the model's predictions on real user input.

**Important:** This is an experimental LSTM-based language model, not a production-grade replacement for modern smartphone keyboards or large language models.

---

## 3. Target Users

### Primary users
- Students learning deep learning and NLP.
- Developers exploring LSTM-based language models.
- Recruiters reviewing machine learning and full-stack portfolios.
- Users interested in experimenting with next-word prediction.

### User needs
- Enter text and obtain predictions quickly.
- See alternative candidate words.
- Understand how the prediction model works.
- Experiment with different input sequences.
- Access the application from desktop and mobile devices.

---

## 4. Technology Stack

### Frontend
- Next.js with App Router
- TypeScript
- Tailwind CSS
- React
- Fetch API for backend communication

### Backend
- Python
- FastAPI
- Pydantic
- Uvicorn

### Machine Learning
- TensorFlow/Keras
- Custom-trained LSTM model
- WikiText-103 dataset
- Vocabulary-based tokenization

### Storage
- Google Drive during development
- Hugging Face Hub or cloud object storage for deployment artifacts

### Deployment
- Vercel for the Next.js frontend
- A compatible Python hosting platform for FastAPI
- GitHub for source control and CI/CD

### Architecture

```text
                  USER
                    |
                    v
             NEXT.JS FRONTEND
               (Vercel)
                    |
                    | HTTPS POST /predict
                    v
              FASTAPI BACKEND
                    |
                    v
             TEXT PREPROCESSING
                    |
                    v
             TOKENIZER / VOCAB
                    |
                    v
              TRAINED LSTM
                    |
                    v
             PREDICTION ENGINE
                    |
                    v
             JSON RESPONSE
                    |
                    v
             NEXT.JS INTERFACE
```

---

## 5. Functional Requirements

### FR-01: Text Input

The application must provide a text input area where users can enter a sentence or paragraph.

Requirements:
- Support normal English text.
- Allow users to edit and clear their input.
- Provide a sample sentence for first-time users.
- Validate empty input.
- Limit the request length to prevent unnecessarily large requests.

### FR-02: Next-Word Prediction

The user must be able to request the next-word prediction.

Workflow:
1. User enters text.
2. Frontend sends the text to the backend.
3. Backend preprocesses the input using the same rules used during training.
4. Input text is tokenized using the saved vocabulary.
5. The sequence is converted into token IDs.
6. The sequence is truncated or padded to 30 tokens.
7. The LSTM predicts probabilities for the vocabulary.
8. The backend returns the predicted word.
9. The frontend displays the result.

Endpoint:

`POST /predict`

Request:

```json
{
  "text": "Machine learning is a"
}
```

Response:

```json
{
  "input": "Machine learning is a",
  "predicted_word": "powerful",
  "confidence": 0.24
}
```

The response values above are illustrative, not actual model output.

### FR-03: Alternative Predictions

The application should display the top three candidate words.

Example:

```json
{
  "predictions": [
    {
      "word": "powerful",
      "probability": 0.24
    },
    {
      "word": "useful",
      "probability": 0.17
    },
    {
      "word": "common",
      "probability": 0.11
    }
  ]
}
```

The backend should calculate these alternatives from the model's output probabilities.

### FR-04: Interactive Prediction

Users should be able to request another prediction after modifying their text.

Optional enhancement:
- Add a button to append the selected word to the input.
- Allow users to generate the next prediction using the updated context.
- Repeat this process to create a longer sequence.

### FR-05: Model Information

The application should include an About Model section containing:
- Model architecture: LSTM.
- Training dataset: WikiText-103.
- Input sequence length: 30 tokens.
- Vocabulary size: approximately 30,000 tokens.
- Embedding dimension: 128.
- LSTM layers: two, with 128 units each.
- Output: next-token probability distribution.

Display training metrics only after they have been measured and verified.

### FR-06: Health Check

The backend must expose a health endpoint.

`GET /health`

Example response:

```json
{
  "status": "healthy",
  "model_loaded": true
}
```

The endpoint should indicate whether the model is available for inference.

### FR-07: Error Handling

The application must handle:
- Empty text input.
- Invalid request payloads.
- Backend connection failures.
- Model loading failures.
- Prediction timeouts.
- Unexpected server errors.

The frontend should display understandable error messages without exposing internal stack traces.

---

## 6. User Interface Requirements

### Page 1: Home / Predictor

Route: `/`

Components:
- Navigation bar with product name.
- Hero heading: "Predict the next word with AI."
- Short product description.
- Main text input area.
- Predict button.
- Predicted word display.
- Top-three suggestions.
- Loading indicator.
- Error state.
- Example input buttons.

### Page 2: How It Works

Route: `/how-it-works`

Sections:
- What is next-word prediction?
- What is an LSTM?
- How tokenization works.
- Why embeddings are needed.
- How the model produces predictions.
- Limitations of the model.

Include a simple architecture diagram.

### Page 3: About Model

Route: `/model`

Display:
- Model architecture.
- Dataset information.
- Vocabulary size.
- Input sequence length.
- Verified training metrics.
- Model limitations.

### UI Design Direction

Use a clean, premium, dark interface.

Suggested design characteristics:
- Dark background with high-contrast typography.
- Subtle gradients and restrained accent colors.
- Rounded cards and clear spacing.
- Highlighted predicted word.
- Responsive layout for mobile and desktop.
- Accessible buttons and input labels.
- Visible loading, success, and error states.

Avoid excessive animation that interferes with text entry.

---

## 7. Backend API Specification

### Endpoint 1: Health Check

`GET /health`

Purpose:
Verify that the backend is running and the model has loaded.

### Endpoint 2: Single Prediction

`POST /predict`

Request:

```json
{
  "text": "The future of artificial intelligence"
}
```

Response:

```json
{
  "predictions": [
    {
      "word": "is",
      "probability": 0.35
    },
    {
      "word": "will",
      "probability": 0.18
    },
    {
      "word": "depends",
      "probability": 0.09
    }
  ]
}
```

The probabilities and candidate words are examples only.

### Endpoint 3: Model Metadata

`GET /model-info`

Example response:

```json
{
  "architecture": "LSTM",
  "sequence_length": 30,
  "vocabulary_size": 30000,
  "embedding_dimension": 128,
  "lstm_layers": 2,
  "lstm_units": 128
}
```

The implementation must derive metadata from the actual deployed model and tokenizer wherever possible.

---

## 8. Machine Learning Integration Requirements

### Model loading

The backend must load the trained model once when the application starts rather than loading it for every request.

### Tokenization consistency

The deployed application must use the exact vocabulary and preprocessing rules used during training.

Required artifacts:
- Trained Keras model.
- `word_to_id` mapping.
- `id_to_word` mapping, or a reliable way to reconstruct it.
- Special-token IDs.
- Text preprocessing and tokenization code.

### Input processing

The model expects a sequence of 30 token IDs.

The backend must:
1. Normalize the input according to training preprocessing.
2. Tokenize the text.
3. Map tokens to vocabulary IDs.
4. Replace unknown words with the saved `<UNK>` ID.
5. Truncate long sequences to the most recent 30 tokens.
6. Apply padding consistent with training.
7. Run inference.
8. Convert predicted token IDs into words.

### Prediction output

The backend should return the top three distinct candidate tokens with their probabilities.

Special tokens such as `<PAD>` and `<UNK>` should not normally be presented as ordinary word suggestions.

### Confidence interpretation

The probability from Softmax represents the model's estimated probability for a candidate within its output distribution. It should not be described as a calibrated measure of real-world correctness.

---

## 9. Non-Functional Requirements

### Performance
- Keep the model loaded between requests.
- Avoid loading the complete training dataset into the inference service.
- Measure prediction latency after deployment.
- Set reasonable request-size and timeout limits.

### Reliability
- Provide a health endpoint.
- Return clear error responses.
- Ensure missing model files are detected at startup.

### Security
- Use HTTPS in production.
- Validate request payloads.
- Restrict request sizes.
- Keep secrets out of frontend source code.
- Apply rate limiting if the public endpoint is exposed.
- Do not log sensitive user text unnecessarily.

### Maintainability
- Separate frontend, API, and model artifacts.
- Use environment variables for service URLs.
- Maintain reproducible dependencies.
- Document how to run and deploy the application.

### Accessibility
- Use semantic HTML.
- Support keyboard navigation.
- Maintain readable contrast.
- Provide accessible loading and error messages.

---

## 10. Deployment Plan

### Frontend deployment
Deploy the Next.js application to Vercel.

Environment variable:

`NEXT_PUBLIC_API_BASE_URL`

This variable should contain the deployed API base URL if the frontend calls FastAPI directly.

Alternatively, use a Next.js Route Handler as a proxy to keep the backend URL server-side.

### Backend deployment
Deploy FastAPI to a Python-compatible hosting service.

Requirements:
- Install Python dependencies.
- Retrieve the model and vocabulary artifacts.
- Load the model during application startup.
- Configure CORS if the frontend calls the API directly.
- Expose the health endpoint.
- Configure an appropriate inference timeout.

### Model artifact storage
Do not rely on files stored only in a temporary Google Colab runtime.

Store the final model and vocabulary in persistent storage, then download or mount them when deploying the backend.

For large artifacts, verify platform storage and memory limits before choosing a host.

---

## 11. Testing Strategy

### Unit tests
- Test text normalization.
- Test tokenization.
- Test unknown-word handling.
- Test sequence padding and truncation.
- Test conversion from token IDs back to words.

### API tests
- Health endpoint returns the correct status.
- Valid prediction requests return candidate words.
- Empty input is rejected.
- Malformed JSON returns a validation error.
- Model-loading failures are handled.

### Integration tests
- Send input from the frontend to FastAPI.
- Confirm the response is rendered correctly.
- Test loading and error states.
- Verify predictions use the saved vocabulary.

### Model evaluation
Evaluate the trained model on a held-out test set.

Report appropriate metrics, such as:
- Top-1 accuracy.
- Top-3 accuracy.
- Validation loss.
- Test loss.
- Prediction latency.

Do not claim model performance before measuring it.

---

## 12. Development Roadmap

### Phase 1: Model artifacts
- Finish model training.
- Save the trained model.
- Export vocabulary mappings.
- Verify that the model loads correctly.
- Test inference in a standalone Python script.

**Deliverable:** A working local prediction function.

### Phase 2: FastAPI backend
- Create the Python backend project.
- Implement model loading.
- Implement `/health`.
- Implement `/predict`.
- Implement `/model-info`.
- Test using the interactive API documentation.

**Deliverable:** A working prediction API.

### Phase 3: Next.js frontend
- Initialize Next.js with TypeScript.
- Configure Tailwind CSS.
- Build the predictor page.
- Connect the frontend to FastAPI.
- Implement suggestions, loading states, and error handling.

**Deliverable:** A working full-stack local application.

### Phase 4: Testing and evaluation
- Test input edge cases.
- Verify vocabulary consistency.
- Measure prediction latency.
- Evaluate the model on held-out data.
- Fix integration issues.

**Deliverable:** A tested application.

### Phase 5: Deployment
- Push the frontend and backend to GitHub.
- Deploy the API.
- Deploy the frontend.
- Configure environment variables and CORS.
- Verify the live application.

**Deliverable:** A publicly accessible application.

---

## 13. Minimum Viable Product (MVP)

The first release is complete when:

- The trained LSTM model loads successfully.
- A user can enter text in the Next.js application.
- The backend returns the top three next-word predictions.
- The frontend displays the predictions.
- Empty inputs and API errors are handled.
- The deployed application works over HTTPS.
- The model and vocabulary persist independently of the Colab runtime.

Advanced features such as user accounts, prediction history, model comparisons, and real-time collaborative writing are outside the initial MVP scope.

---

## 14. Future Enhancements

After the MVP is working, consider:
- Autocomplete that appends the selected word.
- Temperature-based sampling.
- Prediction history stored locally in the browser.
- Comparison with a baseline n-gram model.
- Model evaluation dashboards.
- A Transformer-based model for comparison.
- Docker Compose for local development.
- GitHub Actions for automated tests and deployment checks.

---

## 15. Success Criteria

The project will be considered successful when:
1. The model can be loaded independently of the training notebook.
2. The API consistently returns valid predictions.
3. The frontend correctly displays those predictions.
4. The deployed application is accessible from a browser.
5. The reported metrics come from actual evaluation.
6. The repository includes setup and deployment instructions.

**Final architecture:** Next.js + TypeScript + Tailwind CSS + FastAPI + TensorFlow/Keras + persistent model artifacts.