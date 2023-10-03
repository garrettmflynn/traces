const sidecarMessage = document.getElementById('sidecar-msg') as HTMLElement
const display = (message: string) => {
  sidecarMessage.innerHTML += `<p>${message}</p>`
}

const clear = () => sidecarMessage.innerText = ''

Plotly.newPlot('plotly', []);

const updatePlot = ({ data, timestamps }: any) => {
  Plotly.react('plotly', data.map(channel => {
    return {
      x: timestamps,
      y: channel,
      type: 'scatter',
      showlegend: false,
      hoverinfo:'skip'
    }
  }, []))
}




const pythonUrl = new URL(COMMONERS.services.python.url) // Equivalent to commoners://python

const button = document.querySelector('button') as HTMLButtonElement
const input = document.querySelector('input') as HTMLInputElement
button.onclick = () => {
  onSubmit(input.value)
}


async function post(url: string | URL, payload: any) {

  const start = performance.now()
  const res = await fetch(
    url, 
    {
      method: "POST", 
      body: JSON.stringify(payload)
    }
  )
  .then(res => res.json())

  console.log(`Time to run: (${url}): ${(performance.now() - start).toFixed(3)}ms`)

  return res
}

const onSubmit = async(s3_url: string) => {


  clear()
  display(`Attempting to Initialize: <small>${s3_url}</small>`)

  await post(
    new URL('init', pythonUrl), 
    { s3_url }
  )
  .then(async (metadata) => {

    display(`Initialized: <small>${JSON.stringify(metadata)}</small>`)

    const user_opts = {
      s3_url,
      start_time: 0,
      end_time: 1,
      channel_indices: Array.from({length: 25 }, (_,i) => i)
    }

    await post(
      new URL('get', pythonUrl), 
      user_opts
    )
    .then((res) => {
      updatePlot(res)
    })
  })
}

