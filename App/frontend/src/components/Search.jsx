import React from 'react'
import DashVideoPlayer from './DashVideoPlayer.jsx';
import Videos from './Videos.jsx';

export default function Search({ videos, clickedSearch, setSelectedText, selectedText }) {
    const metadata = {
        'class_title': 'Class Title',
        'professor': 'Professor',
        'subject': 'Subject',
        'school_year': 'School Year'
    };
    return (
        <>
            {
                videos.length == 0 || clickedSearch == false ?
                    <div></div> :
                    <Videos videos={videos} metadata={metadata} setSelectedText={setSelectedText} selectedText={selectedText} />
            }
        </>
    )
}
