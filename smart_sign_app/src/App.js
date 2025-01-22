import React from 'react';
import ElectricalSign from './components/electricalSign';
import CharacterCalculator from './components/characterCalculator';
import TestSize from './components/sizetest'
import Forms from './components/forms';
import Homep from './Homep';
import CastomerTrip from './components/castomerTrip';
import FieldCheck from './components/fieldCheck';
import PassengerInfoSign from './components/PassengerInfoSign ';

import {
  BrowserRouter,
  Routes,
  Route,
  redirect as Redirect,
  Navigate,
} from "react-router-dom";
const App = () => {
  
  return (
    // <div>
    //   <ElectricalSign />
    // </div>
    <>
     <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/home" replace />} />{
            <Route path="/home" element={<Homep />} />}
          { <Route path="/electricalSign" element={<ElectricalSign />} /> }
//          <Route path="/electricalSign" element={<PassengerInfoSign />} />
          <Route path="/characterCalculator" element={<CharacterCalculator />} />
          <Route path='TestSize' element={< TestSize/>} />
          <Route path="/Forms" element={<Forms />} />
            <Route path="/fieldCheck" element={<FieldCheck />} />
            <Route path="/castomerTrip" element={<CastomerTrip />} />
          
          {/* <Route path="/application/:id" element={<Application />}>
            <Route
              index
              path="/application/:id/details"
              element={<Details />}
            />
            <Route path="/application/:id/payment" element={<PaymentPage />} />
            <Route path="/application/:id/reports" element={<Reports />} />
            <Route
              path="/application/:id/goodReport/:reportMessage"
              element={<GoodReport />}
            />
          </Route>
          <Route
            path="/application/:id/goodPayment"
            element={<GoodPayment />}
          />
          <Route path="/m-application/:id" element={<ManagerApplication />}>
            <Route
              path="/m-application/:id/managerReports"
              element={<MReports />}
            />
            <Route
              path="/m-application/:id/management"
              element={<Management />}
            />

            <Route
              path="/m-application/:id/managerPayment"
              element={<MPayment />}
            />
            <Route path="/m-application/:id/details" element={<MDetails />} />
          </Route>
          <Route path="*" element={<NotFound />}></Route>  */}
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
