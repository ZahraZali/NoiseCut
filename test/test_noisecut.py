
def test_noisecut():

    component = 0
    stream = read(file)
    trace = stream[component]
    
    filtered_trace, spectrogram = noisecut(trace, plotspec=True)


    plot(filtered_trace, spectrogram)




