let checkboxes = document.getElementsByName('chbxs')
console.log(checkboxes)

let form = {
    stepOne: [],
}

checkboxes.forEach(bx => {
    bx.addEventListener('click', (x) => {
        form.stepOne.push(bx.value)
    })
})

let btn = document.getElementById('btn')

btn.addEventListener('click', async () => {
    console.log(form)
    const res = await fetch('http://dupa.com/app1/addDonation', {
        method: 'POST',
        body: JSON.stringify(form)
    }).then(res => res.json())


    console.log(res)
})