# note for design

## stuff to do in the python side

## rough design in the python API side

- AudioSegment
    - immutuable in-memory data structure
    - hold its own metadata and data
        - metadata stored as a pydantic object
          - alt: dataclass or namedtuple to avoid dependecy
        - data stored as a numpy multi dimensional array
          - alt: python native array to avoid dependency
    - provdde a set of easy help function to perform common easy anaysis and manipulation of audio
        - note: could check pydub to understand more
        - for example
          - get metadata, get derived metadata,
          - get data, get subset data by time(s) or frame(s)
          - get slice
          - ops: up/down volume, extend/shorten time, mix, add-white-noise, etc.
          - write
    - as an interface to other more complex stand-alone tools for complex audio analysis and manipulation
        - note: could check some of SOTA audio deeplearning models to see what would be the common pattern
    - what need to be de-risked and tried before we finalize the design
        - what info needed to be presented in the actual data so to make the data structure easy usable?
          - are those essential or just good to have?
            - channel
            - frame
        - how to decide the value dtype for the actual data stored?
        - what metadata would be needed in the actual data to make things easily usable?
            - what is essential and need to be there for an in-mem data structure? what are only needed for file IO and even for specific type of file IO?
            - total length? number of frames? length of frame?
        - should we have an immutable and a mutable class?
            - prob yes but later
        - how to design a good gereric data structrue to represent an audio segment
            - notice no need to worry about compression and some other properties
            - as those should be considered as properties for specifc audio file
- AudioFileReader
  - interface to allow reading from an audio file
    - simplest case: just read the whole file and create the corresponding AudioSegment
    - more complex case: open a file, read the metadata, seek and read a subset of the data and return as AudioSegment
    - even more complex: open a file, read the metadata, then hold the file handler
      - provide interface to read a specified subset as a AudioSegment
      - provide interface to streaming read a specified subset as a generator of several AudioSegments
    - we might want to start with only supporting wav for the beginning
- AudioFileWriter
  - interface to allow writing AudioSegment(s) to an audio file
    - simplest case: given one audio segment, and some control paramters, write to an audio file
    - more complex case: given a stream of audio segments, streaming write to an audio file, and finally commit the whole change
      - ddpends on the destination format