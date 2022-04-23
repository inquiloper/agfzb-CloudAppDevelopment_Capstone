/**
 * Get all dealerships
 */

const Cloudant = require('@cloudant/cloudant');


async function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });


    try {
        const db = cloudant.db.use('dealerships');

        let results = [];
        let rows = [];
        
        if (params.state) {
            results = await db.find(
                {
                    "selector": {
                        "st": {"$eq": params.state}
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
