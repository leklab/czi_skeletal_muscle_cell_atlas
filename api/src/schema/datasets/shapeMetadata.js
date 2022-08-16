const shapeMetadata = () => {
  

	console.log("In function")

  	return esHit => {
    // eslint-disable-next-line no-underscore-dangle
    const metadata = esHit._source
    console.log(metadata)
    
	    return {
	    	cell_id: metadata.cell_id,
	    	age: metadata.age,
	    	sex: metadata.sex,
	    }
  	}



}

export default shapeMetadata