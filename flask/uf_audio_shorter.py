from flask import Flask, Response

app = Flask(__name__)


@app.route("/")
def audio():
    def wav_generator(sample_rate=8000, seconds=300, samples=1024):
        yield b"RIFF$\x00}\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00@\x1f"
        yield b"\x00\x00@\x1f\x00\x00\x01\x00\x08\x00data\x00\x00}\x00"
        for i in range(0, sample_rate * seconds, samples):
            yield bytes(
                (t * ((t >> 9 | t >> 13) & 15)) & 129 for t in range(i, i + samples)
            )

    return Response(wav_generator(), mimetype="audio/x-wav;codec=pcm")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, threaded=True)
