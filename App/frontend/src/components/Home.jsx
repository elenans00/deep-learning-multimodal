import React, { useEffect, useState } from 'react';
import Searcher from './Searcher.jsx';
import Question from './Question.jsx';
import Search from './Search.jsx';

export default function Home() {
  const [inputText, setInputText] = useState("");
  const [videos, setVideos] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedText, setSelectedText] = useState("");
  const [clickedSearch, setClickedSearch] = useState(false);
  const [clickedQuestion, setClickedQuestion] = useState(false);
  const [answer, setAnswer] = useState({});
  const [contextAnswer, setContextAnswer] = useState([]);

  function handleChangeInput(event) {
    setInputText(event.target.value);
  }

  function handleClickSearch() {
    setClickedQuestion(false);
    setClickedSearch(true);
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://127.0.0.1:8000/search?text_input=${inputText}`);
        const result = await response.json();
        let aux = [];
        const vids = result['data']['Get']['Video'];
        for (const idx in vids) {
          aux.push({
            'url': vids[idx]['url'],
            'startTime': vids[idx]['start'],
            'endTime': vids[idx]['end'],
            'metadata': vids[idx]['metadata'],
            'text': vids[idx]['text'],
            'id': idx
          })
        }
        setVideos(aux);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }

  function handleClickQuestion() {
    setClickedSearch(false);
    setClickedQuestion(true);
    setAnswer("");
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://127.0.0.1:8000/question?text_input=${inputText}`);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const result = await response.json();
        const aux = result['data']['Get']['Answer'];
        setAnswer(aux)
        let metadata = [];
        const vids = result['data']['Get']['Video'];
        for (const idx in vids) {
          metadata.push({
            'text': vids[idx]['text'],
            'url': vids[idx]['url'],
            'metadata': vids[idx]['metadata'],
            'startTime': vids[idx]['start'],
            'endTime': vids[idx]['end'],
          })
        }
        setContextAnswer(metadata);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }

  return (
    <div className='w-full h-full bg-white px-24 py-12'>
      <Searcher inputText={inputText} handleChangeInput={handleChangeInput} handleClickSearch={handleClickSearch} handleClickQuestion={handleClickQuestion} />
      <div className='h-12 bg-white' />
      <div className='bg-slate-200 rounded-md shadow-md border-4 py-24 px-20'>
        <Question clickedQuestion={clickedQuestion} loading={loading} answer={answer} contextAnswer={contextAnswer} selectedText={selectedText} setSelectedText={setSelectedText}/>
        <Search videos={videos} clickedSearch={clickedSearch} setSelectedText={setSelectedText} selectedText={selectedText} />
      </div>
    </div >
  )
}
