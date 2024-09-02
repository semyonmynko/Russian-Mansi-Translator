import React, { useState } from 'react';
import axios from 'axios';

const TranslationComponent = () => {
    const [text, setText] = useState('');
    const [translatedText, setTranslatedText] = useState('');
    const [sourceLanguage, setSourceLanguage] = useState('Mansi');
    const [targetLanguage, setTargetLanguage] = useState('Russian');
    const [loading, setLoading] = useState(false);

    const handleTranslate = async () => {
        setLoading(true);
        try {
            const response = await axios.post('http://localhost:8000/translate', {
                text,
                source_language: sourceLanguage,
                target_language: targetLanguage,
            });
            setTranslatedText(response.data.translated_text);
        } catch (error) {
            console.error('Error during translation:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Translation Service</h1>
            <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Enter text to translate"
            />
            <button onClick={handleTranslate}>Translate</button>
            {loading ? <p>Loading...</p> : <p>Translated Text: {translatedText}</p>}
        </div>
    );
};

export default TranslationComponent;
