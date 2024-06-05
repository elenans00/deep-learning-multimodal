import React from 'react'
import Videos from './Videos.jsx';

export default function Question({ clickedQuestion, loading, answer, contextAnswer, selectedText, setSelectedText }) {
    const metadata = {
        'class_title': 'Class Title',
        'professor': 'Professor',
        'subject': 'Subject',
        'school_year': 'School Year'
    };
    return (
        <div>
            {clickedQuestion == false ?
                "" :
                (loading == true ?
                    (
                        <div className='h-full w-full flex items-center justify-center'>
                            <span className="loading loading-ball loading-lg"></span>
                        </div>
                    ) :
                    (
                        <div>
                            <div className='w-full items-center justify-center flex'>
                                <div className='grid gap-y-2 bg-slate-50 p-12 rounded-sm shadow-md border-4'>
                                    <h1 className='text-xl font-semibold'> Answer: </h1>
                                    <p>
                                        {answer}
                                    </p>
                                </div>
                            </div>
                            <div className='py-8'>
                                <h1 className='text-xl font-semibold'> Based on: </h1>
                            </div>
                            <Videos videos={contextAnswer} setSelectedText={setSelectedText} selectedText={selectedText} metadata={metadata}/>
                        </div>

                    )
                )
            }
        </div>
    )
}
