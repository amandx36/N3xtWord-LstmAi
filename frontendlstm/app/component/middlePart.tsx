export default function Middlepart() {
    return (
        <>
            <div>
                <label htmlFor="userInput">
                    Enter the text to predict the next words using LSTM.
                </label>

                <input
                    id="userInput"
                    type="text"
                    placeholder="Start typing here..."
                />
            </div>
        </>
    );
}