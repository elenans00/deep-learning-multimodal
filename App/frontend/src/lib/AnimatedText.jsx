import React, { useRef } from "react";
import { motion, useInView } from "framer-motion";

const defaultAnimations = {
  hidden: {
    opacity: 0,
  },
  visible: {
    opacity: 1,
    transition: {
      duration: 0.01
    }
  },
}

export default function AnimatedText({ text, className, once }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { amount: 0.8, once: once })
  return (
    <motion.p
      ref={ref}
      initial="hidden"
      animate={isInView ? "visible" : "hidden"}
      transition={{ staggerChildren: 0.15 }}
      className={className}>
      {text.split(" ").map((word) => (
        <span className="inline-block">
          {word.split("").map((char) => (
            <motion.span className="inline-block" variants={defaultAnimations}>
              {char}
            </motion.span>
          ))}
          <span className="inline-block">&nbsp;</span>
        </span>
      ))}
    </motion.p>
  )
}
