#!/usr/bin/env runhaskell

import Control.Monad
import System.Process
import System.IO

import System (readSystem,readSystem0)

main :: IO ()
main = do
  csrcs <- readSystem0 "find | grep '\\.c$'"
  forM_  (lines csrcs) $ \ fn -> do
    putStrLn fn
