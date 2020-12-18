import io
import struct

from flask import Flask, Response, render_template_string

app = Flask(__name__)


def gen_header(sample_rate, bytes_per_sample, channels, samples):
    buf = io.BytesIO()
    buf.write(b"RIFF")
    data_size = samples * channels * bytes_per_sample
    buf.write(struct.pack("<i", data_size + 36))
    buf.write(b"WAVEfmt ")
    buf.write(
        struct.pack(
            "<ihHIIHH",
            16,
            1,
            channels,
            sample_rate,
            (sample_rate * channels * bytes_per_sample),
            (channels * bytes_per_sample),
            bytes_per_sample * 8,
        )
    )
    buf.write(b"data")
    buf.write(struct.pack("<i", data_size))
    return buf.getvalue()


@app.route("/audio")
def audio():
    def wav_generator(
        samples=1024, sample_rate=8000, bytes_per_sample=1, channels=1, seconds=300
    ):
        f = lambda t: (t * ((t >> 9 | t >> 13) & 15)) & 129
        max_value = 2 << (bytes_per_sample * 8 - 1)
        yield gen_header(sample_rate, bytes_per_sample, channels, samples * sample_rate)
        for i in range(0, sample_rate * seconds, samples):
            data = b"".join(
                (f(t) % max_value).to_bytes(bytes_per_sample, "big")
                for t in range(i, i + samples)
            )
            yield data

    return Response(wav_generator(), mimetype="audio/x-wav;codec=pcm")


@app.route("/")
def index():
    return render_template_string(
        '<audio controls autoplay loop><source src="{{ url_for("audio") }}" />'
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, threaded=True)
