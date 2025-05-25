import { useState, useEffect } from "react";
import {
  Container,
  Typography,
  Box,
  CircularProgress,
  Grid,
  useTheme,
} from "@mui/material";
import { motion } from "framer-motion";
import CollectionEfficiencyChart from "./components/Dashboard/CollectionEfficiencyChart";
import CollectionTrendsChart from "./components/Dashboard/CollectionTrendsChart";
import PerformanceInsights from "./components/Dashboard/PerformanceInsights";
import { fetchCollectionStats } from "./services/api";

const MotionContainer = motion(Container);

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const theme = useTheme();

  useEffect(() => {
    const loadData = async () => {
      try {
        const stats = await fetchCollectionStats();
        setData(stats);
      } catch (err) {
        setError("Error al cargar los datos");
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
        bgcolor={theme.palette.background.default}
      >
        <CircularProgress size={60} />
      </Box>
    );
  }

  if (error) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
        bgcolor={theme.palette.background.default}
      >
        <Typography color="error" variant="h5">
          {error}
        </Typography>
      </Box>
    );
  }

  return (
    <MotionContainer
      maxWidth="xl"
      sx={{
        py: 4,
        minHeight: "100vh",
        bgcolor: theme.palette.background.default,
      }}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <Typography
        variant="h3"
        component="h1"
        gutterBottom
        sx={{
          textAlign: "center",
          mb: 4,
          color: theme.palette.primary.main,
          fontWeight: "bold",
        }}
      >
        Dashboard de Cobranza
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} lg={8}>
          <CollectionEfficiencyChart data={data} />
        </Grid>
        <Grid item xs={12} lg={4}>
          <PerformanceInsights data={data} />
        </Grid>
        <Grid item xs={12}>
          <CollectionTrendsChart data={data} />
        </Grid>
      </Grid>
    </MotionContainer>
  );
}

export default App;
