import React from 'react'

export default function Searcher({ inputText, handleChangeInput, handleClickSearch, handleClickQuestion }) {
    return (
        <div className='bg-slate-200 rounded-md shadow-md border-4 py-24'>
            <div className='w-full items-center flex justify-center pb-24'>
                <h1 className='text-3xl font-bold'>
                    Search Videos or Ask a Question
                </h1>
            </div>

            <div className='w-full items-center justify-center flex'>
                <div className='grid grid-cols-1 gap-y-4 py-4'>
                    <input
                        type='text'
                        value={inputText}
                        onChange={handleChangeInput}
                        placeholder='Please enter the text...'
                        className="input input-bordered w-[500px]"
                    />
                    <div className='flex gap-x-4 items-center justify-center'>
                        <button
                            className="btn btn-accent w-24"
                            onClick={() => handleClickSearch()}
                        >
                            Search
                        </button>
                        <button
                            className="btn btn-accent w-24"
                            onClick={() => handleClickQuestion()}
                        >
                            Question
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}
