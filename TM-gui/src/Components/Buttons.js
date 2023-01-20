export function ButtonRounded({addTaskFunc}){
    return (
        <button onClick={addTaskFunc} type="button" className='btn btn-lg btn-success round'>+</button>
    );
}

export default ButtonRounded;