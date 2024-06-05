import React from 'react'
import DashVideoPlayer from './DashVideoPlayer.jsx';


export default function Videos({ videos, metadata, setSelectedText, selectedText }) {
    return (
        <div className='grid grid-cols-1 gap-y-8 gap-x-8'>
            {
                videos.map((item) => (
                    <div>
                        <div className="card lg:card-side bg-base-100 shadow-xl">
                            <figure><DashVideoPlayer url={'/videos/' + item.url} startTime={item['startTime']} endTime={item['endTime']} /></figure>
                            <div className="card-body">
                                {
                                    Object.keys(metadata).map((key) => (
                                        <p>
                                            {metadata[key]}: {item['metadata'][key]}
                                        </p>
                                    ))
                                }
                                <div className='h-8' />
                                <div className="card-actions justify-between">
                                    <button
                                        className="btn"
                                        onClick={() => {
                                            setSelectedText(item['text']);
                                            document.getElementById('my_modal_2').showModal();
                                        }}
                                    >Show Text</button>
                                    <dialog id="my_modal_2" className="modal">
                                        <div className="modal-box">
                                            <div className='overflow-auto'>
                                                <p className="py-4">{selectedText}</p>
                                            </div>
                                        </div>
                                        <form method="dialog" className="modal-backdrop">
                                            <button>close</button>
                                        </form>
                                    </dialog>
                                </div>
                            </div>
                        </div>
                    </div>
                ))
            }
        </div>
    )
}