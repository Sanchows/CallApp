import asyncio
import pyaudio

class Main():
    async def tcp_echo_client(self):

        reader, writer = await asyncio.open_connection(
            'localhost', 8888   )
        #####
        p_input = pyaudio.PyAudio()
        chunk_input = 128
        stream_input = p_input.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100, 
            input = True,
            frames_per_buffer = chunk_input)
        #####
        p_output = pyaudio.PyAudio()
        chunk_output = 128
        stream_output = p_output.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            output=True,        
            frames_per_buffer=chunk_output)
        #####
        while True:
            writer.write(stream_input.read(chunk_input))
            await writer.drain()

            data = await reader.read(256)
            stream_output.write(data)
            

        print('Close the connection')
        writer.close()

asyncio.run(Main().tcp_echo_client())
