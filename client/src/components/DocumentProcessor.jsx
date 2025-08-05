import React, { useState } from 'react';
import { FileText, Send, Loader } from 'lucide-react';
import { chatAPI } from '../services/api';

const DocumentProcessor = ({ onResults }) => {
    const [questions, setQuestions] = useState(['']);
    const [isLoading, setIsLoading] = useState(false);
    const [results, setResults] = useState(null);

    const addQuestion = () => {
        setQuestions([...questions, '']);
    };

    const updateQuestion = (index, value) => {
        const newQuestions = [...questions];
        newQuestions[index] = value;
        setQuestions(newQuestions);
    };

    const removeQuestion = (index) => {
        if (questions.length > 1) {
            const newQuestions = questions.filter((_, i) => i !== index);
            setQuestions(newQuestions);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (questions.every(q => !q.trim())) return;

        setIsLoading(true);
        try {
            const validQuestions = questions.filter(q => q.trim());
            // Send dummy document URL since your data is in Discovery Engine
            const response = await chatAPI.processQuestions("knowledge_base", validQuestions);
            
            if (response.success) {
                setResults({
                    questions: validQuestions,
                    answers: response.answers
                });
                onResults && onResults(response.answers);
            } else {
                throw new Error(response.error || 'Failed to process questions');
            }
        } catch (error) {
            console.error('Error processing questions:', error);
            setResults({
                error: error.message || 'Failed to process questions'
            });
        } finally {
            setIsLoading(false);
        }
    };

    const loadSampleQuestions = () => {
        setQuestions([
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?",
            "What is the waiting period for cataract surgery?",
            "Are the medical expenses for an organ donor covered under this policy?"
        ]);
    };

    return (
        <div className="max-w-4xl mx-auto p-6">
            <div className="bg-white rounded-lg shadow-lg">
                <div className="px-6 py-4 border-b border-gray-200">
                    <div className="flex items-center space-x-2">
                        <FileText className="text-blue-500" size={24} />
                        <h2 className="text-xl font-semibold text-gray-900">Knowledge Base Q&A</h2>
                    </div>
                    <p className="text-gray-600 mt-1">
                        Ask questions about your trained dataset - no document upload needed!
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-6">
                    {/* Info Banner */}
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <div className="flex items-center space-x-2">
                            <FileText className="text-blue-600" size={16} />
                            <p className="text-blue-800 text-sm">
                                <strong>Your data is ready!</strong> This system uses your pre-trained Google Discovery Engine 
                                with your PDF datasets stored in Google Cloud. Just ask your questions below.
                            </p>
                        </div>
                    </div>

                    {/* Questions Input */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Questions for your Knowledge Base
                        </label>
                        <div className="space-y-3">
                            {questions.map((question, index) => (
                                <div key={index} className="flex space-x-2">
                                    <input
                                        type="text"
                                        value={question}
                                        onChange={(e) => updateQuestion(index, e.target.value)}
                                        placeholder={`Question ${index + 1}...`}
                                        className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    />
                                    {questions.length > 1 && (
                                        <button
                                            type="button"
                                            onClick={() => removeQuestion(index)}
                                            className="px-3 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                                        >
                                            ×
                                        </button>
                                    )}
                                </div>
                            ))}
                            <button
                                type="button"
                                onClick={addQuestion}
                                className="text-blue-600 hover:text-blue-700 text-sm font-medium"
                            >
                                + Add another question
                            </button>
                        </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex justify-between">
                        <button
                            type="button"
                            onClick={loadSampleQuestions}
                            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                        >
                            Load Sample Questions
                        </button>
                        
                        <button
                            type="submit"
                            disabled={isLoading || questions.every(q => !q.trim())}
                            className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                        >
                            {isLoading ? (
                                <>
                                    <Loader className="animate-spin" size={16} />
                                    <span>Processing...</span>
                                </>
                            ) : (
                                <>
                                    <Send size={16} />
                                    <span>Ask Questions</span>
                                </>
                            )}
                        </button>
                    </div>
                </form>

                {/* Results */}
                {results && (
                    <div className="px-6 pb-6">
                        <div className="border-t pt-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">Results from Knowledge Base</h3>
                            
                            {results.error ? (
                                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                                    <p className="text-red-800">{results.error}</p>
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    {results.questions.map((question, index) => (
                                        <div key={index} className="bg-gray-50 rounded-lg p-4">
                                            <h4 className="font-medium text-gray-900 mb-2">
                                                Q{index + 1}: {question}
                                            </h4>
                                            <div className="bg-white rounded-lg p-3 border">
                                                <p className="text-gray-700 leading-relaxed">
                                                    {results.answers[index]}
                                                </p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default DocumentProcessor;
