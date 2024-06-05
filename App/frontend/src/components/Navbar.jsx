import React from 'react'
import Logo from '/public/logo.webp'
import { Link } from 'react-router-dom'

export default function Navbar() {
    return (
        <div className="navbar sticky bg-black/30 backdrop-blur-sm top-0 z-20 bg-base-100">
            <div className="flex-1">
                <button
                    className="btn btn-ghost text-xl text-black"
                    onClick={() => window.scrollTo(0,0)}
                >
                    TFG Elena
                </button>
            </div>
            <div className="flex-none">
                <Link to="https://www.um.es/">
                    <button className="btn btn-square btn-ghost w-48">
                        <img src={Logo} className='' />
                    </button>
                </Link>
            </div>
        </div>
    )
}
