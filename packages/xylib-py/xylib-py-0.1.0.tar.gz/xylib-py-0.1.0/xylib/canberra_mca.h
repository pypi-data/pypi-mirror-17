// Canberra AccuSpec MCA
// Licence: Lesser GNU Public License 2.1 (LGPL)

// based on a chapter from an unknown instruction, pages B1-B5:
// APPENDIX B: FILE STRUCTURES
// "Spectral data acquired on the MCA system are directly
// accumulated in memory. These data are transferred to a disk
// file via the \Move command in the MCA program."
//
// This format is (was?) used in two synchrotron stations in Hamburg.
// Data is produced by Canberra multi-channel analyser (MCA).
// NOTE: .mca is not a canonical extension.
// Update: In Cambio software from sandia.gov this format is called
//         Canberra Accuspec (*.dat). In ver. 0.9 .dat extension was added.


#ifndef XYLIB_CANBERRA_MCA_H_
#define XYLIB_CANBERRA_MCA_H_
#include "xylib.h"

namespace xylib {

    class CanberraMcaDataSet : public DataSet
    {
        OBLIGATORY_DATASET_MEMBERS(CanberraMcaDataSet)
    public:
        static double pdp11_f (char* p);
    };

}
#endif // CANBERRA_MCA_H_

