/**
 * Get all reviews
 */

 const Cloudant = require('@cloudant/cloudant');


 async function main(params) {
     const cloudant = Cloudant({
         url: params.COUCH_URL,
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
     });
 
 
     try {
         const db = cloudant.db.use('reviews');
 
         let results = [];
         let rows = [];
         
         if (params.dealerId) {
             results = await db.find(
                 {
                     "selector": {
                         "dealership": {"$eq": parseInt(params.dealerId)}
                     }
                 }
             );
             rows = results.docs;
         } else {
             results = await db.list({include_docs: true});
             results.rows.forEach(async (row) => {
                 rows.push(row.doc);
             })
         }
 
 
         return {
             code: 0,
             data: rows
         }
    } catch (error) {
            return { error: error };
        }

}
